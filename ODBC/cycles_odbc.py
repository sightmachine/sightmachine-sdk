import os
import sys
import pyodbc
import logging
import functools
import pandas as pd
import typing as t_
import time
from smsdk import client
from datetime import datetime, timedelta


log = logging.getLogger(__name__)


def log_or_print(msg, log=None, type: str = None):
    """Log a message if log is provided, otherwise print it."""
    if log is None:
        print(msg)
    else:
        if type is None or type == "info":
            log.info(msg)
        elif type == "warning":
            log.warning(msg)
        elif type == "error":
            log.error(msg)
        else:
            raise Exception(
                f"Unknown log type: {type} - must be 'info', 'warning', 'error', or None."
            )


def connect_with_retries(
    conn_str: str, max_retries: int = 3, delay_seconds: int = 5
) -> t_.Optional[pyodbc.Connection]:
    """Attempts to establish a database connection with configurable retries.

    Args:
        conn_str: The connection string for the database.
        max_retries: The maximum number of retries to attempt. Defaults to 3.
        delay_seconds: The number of seconds to wait between retries. Defaults to 5.

    Returns:
        The database connection object if successful, otherwise None.
    """

    for attempt in range(0, max_retries):
        try:
            conn = pyodbc.connect(conn_str)
            return conn  # Connection successful, return the connection object

        except Exception as ex:
            log_or_print(
                f"Error:: {str(ex)} :: Connection to the DB failed on attempt {attempt + 1}/{max_retries}. Retrying in {delay_seconds} seconds.",
                log,
                "error",
            )
            time.sleep(delay_seconds)  # Wait before retrying

    # All retries failed, log a final error message
    log_or_print(
        f"Error:: Connection to the DB failed after {max_retries} retries.",
        log,
        "error",
    )
    return None


def connect_to_db() -> (
    t_.Tuple[t_.Optional[pyodbc.Connection], t_.Optional[pyodbc.Cursor]]
):
    conn = None
    cursor = None

    driver = "{PostgreSQL Unicode}"
    port = 5432
    sdk_tenant = os.environ.get("ENV_VAR_TENANT")
    key_id = os.environ.get("ENV_VAR_API_KEY")
    secret_id = os.environ.get("ENV_VAR_API_SECRET")

    # Create a connection string for pyodbc
    conn_str = (
        f"DRIVER={driver};"
        f"PORT={port};"
        f"SERVER={sdk_tenant}.sightmachine.io;"
        f"DATABASE=tenant_storage;"
        f"UID={key_id};"
        f"PWD={secret_id};"
        f"SSLmode=require;"
    )

    conn = connect_with_retries(conn_str)

    # Create a cursor from the connection
    if conn:
        cursor = conn.cursor()

    return (conn, cursor)


def disconnect(
    conn: t_.Optional[pyodbc.Connection], cursor: t_.Optional[pyodbc.Cursor]
) -> None:
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def validate_input(func: t_.Callable[..., t_.Any]) -> t_.Callable[..., t_.Any]:
    """This decorator can be used to validate input schema with some conditions,
    or can implement jsonschema validator in later versions if required"""

    @functools.wraps(func)
    def validate(*args: t_.Any, **kwargs: t_.Any) -> t_.Any:
        exceptional_keys = ["_only"]
        for key in kwargs:
            if key in exceptional_keys:
                continue
            if isinstance(kwargs[key], list):
                if not (key.endswith("__in") or key.endswith("__nin")):
                    msg = f"Key <{key}> should end with '__in' or '__nin' if the datatype is list"
                    raise ValueError(msg)
        return func(*args, **kwargs)

    return validate


def get_starttime_endtime_keys(**kwargs: t_.Any) -> t_.Tuple[str, str]:
    """
    This function takes kwargs as input and tried to identify starttime and endtime key provided by user and returns
    :param kwargs:
    :return:
    """
    starttime_key = ""
    endtime_key = ""

    times = {i: kwargs[i] for i in kwargs if "time" in i.lower()}

    if times:
        starttime = min(times.values())
        endtime = max(times.values())

        for key in times:
            if times[key] == starttime:
                starttime_key = key
            elif times[key] == endtime:
                endtime_key = key
            else:
                continue

    return starttime_key, endtime_key


# Define a dictionary to map comparison operators
OPERATOR_MAPPING = {
    "gt": ">",
    "lt": "<",
    "gte": ">=",
    "lte": "<=",
    "ne": "<>",
    "eq": "=",
}


def prepare_filter_condition(key_name, key_op, key_val):

    if key_name and key_op and key_val:
        if key_op in OPERATOR_MAPPING:
            # Replace operation with the corresponding symbol
            op = OPERATOR_MAPPING.get(key_op, key_op)

            # Add the condition to the list
            return f""""{key_name}" {op} '{key_val}'"""
        else:
            # Handle unsupported operators
            print(f"Error: Unsupported operator '{key_op}' in where condition.")
    else:
        print(
            f"Error: Missing values for preparing filter condition (name, op, val): ({key_name}, {key_op}, {key_val})."
        )

    return None


@validate_input
def get_cycles(
    cursor: t_.Any,
    client: t_.Any,
    normalize: bool = True,
    clean_strings_in: bool = True,
    clean_strings_out: bool = True,
    *args: t_.Any,
    **kwargs: t_.Any,
) -> pd.DataFrame:
    # When processing in batch
    if args and (not kwargs):
        kwargs = args[0]

    rename_end_time_col = False

    # Get the Machines
    machines = kwargs.pop("machine__source", kwargs.pop("Machine", []))

    if not machines:
        machines = kwargs.pop("machine__source__in", kwargs.pop("Machine__in", []))
        kwargs.pop("machine__source__in", None)
        kwargs.pop("Machine__in", None)

    query_params = {
        "_only": ["source", "source_clean", "source_type"],
        "_order_by": "source_clean",
    }

    if isinstance(machines, str):
        machines = [machines]

    mach_names = client.get_machines(**query_params)
    machmap = {
        mach[1]["source_clean"]: mach[1]["source"] for mach in mach_names.iterrows()
    }

    # Get the machines type
    machine_type = ""

    # it is a list of machines, work with first name in list
    machine_type, machine_schema = client.get_machine_schema(
        machines[0], return_mtype=True
    )
    # converting the UI friendly machine names into the Sight Machine internal names
    machines = [machmap.get(mach, mach) for mach in machines]

    if machine_type.startswith("'") and machine_type.endswith("'"):
        machine_type = machine_type[1:-1]

    # Define a table dynamically based on the columns present in the asset selection
    from_clause = f"sightmachine.cycle_{machine_type}"

    # Convert the internal Sight Machine tag/field names UI friendly tag/field names
    toplevel = {
        "endtime": "End Time",
        "starttime": "Start Time",
        "machine__source": "Machine",
        "total": "Cycle Time (Net)",
        "record_time": "Cycle Time (Gross)",
        "shift": "Shift",
        "output": "Output",
    }

    colmap = {row[1]["name"]: row[1]["display"] for row in machine_schema.iterrows()}
    colmap.update(toplevel)

    # Prepare SQL Query
    sql_query_str = ""
    select_clause_str = ""
    from_clause_str = ""
    where_clause_str = ""
    order_by_clause_str = ""
    limit_clause_str = ""
    offset_clause_str = ""

    select_columns = []

    if not "_only" in kwargs:
        log_or_print("_only not specified. Selecting first 50 fields.", log, "info")
        select_columns = machine_schema["display"].tolist()[:50]
    elif kwargs["_only"] == "*":
        kwargs.pop("_only")
    else:
        select_columns = kwargs.pop("_only", [])

        rename_end_time_col = any(
            column == "End Time" or column == "endtime" for column in select_columns
        )

        # Use list comprehension to perform replacements
        if rename_end_time_col:
            select_columns = [
                "Cycle End Time" if col in {"End Time", "endtime"} else col
                for col in select_columns
            ]

        # Replace 'machine__source' with 'Machine'
        select_columns = [
            "Machine" if col in {"machine__source"} else col for col in select_columns
        ]

        # Check if 'Cycle End Time' is in '_only'
        if "Cycle End Time" not in select_columns:
            log_or_print("Adding 'Cycle End Time' to _only", log, "info")
            select_columns.append("Cycle End Time")

        # Check if 'Machine' is in '_only'
        if "Machine" not in select_columns:
            log_or_print("Adding 'Machine' to _only", log, "info")
            select_columns.append("Machine")

    if len(select_columns):
        available_names = set(
            machine_schema["name"].to_list()
            + machine_schema["display"].to_list()
            + [
                "record_time",
                "total",
                "starttime",
                "output",
                "shift",
            ]
            + [
                "Cycle Time (Gross)",
                "Cycle Time (Net)",
                "Machine",
                "Start Time",
                "Output",
                "Shift",
            ]
        )
        used_names = set(select_columns)
        different_names = used_names.difference(available_names)

        if len(different_names) > 0:
            log_or_print(
                f'Dropping invalid column names: {", ".join(different_names)}.',
                log,
                "info",
            )

        if len(available_names):
            select_columns = [
                colmap.get(col, col) for col in used_names.intersection(available_names)
            ]

    # Generate the SELECT clause based on the 'display' names in the query
    select_clause = ",\n\t".join([f'"{column}"' for column in select_columns])

    # Generate the ORDER BY clause based on the 'order_by' conditions in the query
    order_by_conditions = []
    order_by_values = kwargs.pop("_order_by", [])

    if isinstance(order_by_values, str):
        order_by_values = [order_by_values]

    if len(order_by_values):
        for val in order_by_values:
            prefix = ""
            if val.startswith("-"):
                val = val[1:]
                prefix = "-"
            val = colmap.get(val, val)

            if val == "End Time":
                val = "Cycle End Time"
            if val == "Start Time":
                val = "Cycle Start Time"
            val = colmap.get(val, val)

            if not val in ["Cycle End Time", "Cycle Start Time", "Machine"]:
                log.warn(
                    "Only ordering by 'Start Time', 'End Time' and 'Machine' source currently supported."
                )
                continue

            order_key = f"{prefix}{val}"
            order_key = order_key.replace("_epoch", "")
            order_type = "asc"

            if order_key.startswith("-"):
                order_type = "desc"
                order_key = order_key[1:]
            order_by_conditions.append(f'"{order_key}" {order_type}')
    else:
        order_type = "desc"
        order_key = "Cycle End Time"
        order_by_conditions.append(f'"{order_key}" {order_type}')

    # Replace 'End Time' with 'Cycle End Time' in the keys of the query dictionary
    for key in list(kwargs.keys()):
        if "End Time" in key:
            new_key = key.replace("End Time", "Cycle End Time")
            kwargs[new_key] = kwargs.pop(key)
            rename_end_time_col = True
        if "Start Time" in key:
            new_key = key.replace("Start Time", "Cycle Start Timee")
            kwargs[new_key] = kwargs.pop(key)

    # Generate the WHERE clause based on the 'where' conditions in the query
    where_conditions = []
    etime = datetime.now()
    stime = etime - timedelta(days=1)

    start_key, end_key = get_starttime_endtime_keys(**kwargs)

    starttime = kwargs.pop(start_key, "") if start_key else stime
    name = start_key.split("__")[0]
    op = start_key.split("__")[-1]
    value = starttime.isoformat()

    filter_condition = None
    filter_condition = prepare_filter_condition(name, op, value)

    if filter_condition is not None:
        where_conditions.append(filter_condition)

    endtime = kwargs.pop(end_key, "") if end_key else etime
    name = end_key.split("__")[0]
    op = end_key.split("__")[-1]
    value = endtime.isoformat()

    filter_condition = None
    filter_condition = prepare_filter_condition(name, op, value)

    if filter_condition is not None:
        where_conditions.append(filter_condition)

    for key, val in kwargs.items():
        func = ""
        new_key = key
        filter_condition = None

        # Replace 'End Time' with 'Cycle End Time' in the keys of the query dictionary
        if "End Time" in key:
            new_key = key.replace("End Time", "Cycle End Time")
            rename_end_time_col = True
        elif "Start Time" in key:
            new_key = key.replace("Start Time", "Cycle Start Timee")

        if "__" in new_key:
            parts = new_key.split("__")
            new_key = "__".join(parts[:-1])
            func = parts[-1]

            if not func in [
                "in",
                "nin",
                "gt",
                "lt",
                "gte",
                "lte",
                "exists",
                "ne",
                "eq",
            ]:
                # This isn't actually a function.  Probably another nested item like machine__source
                new_key = f"{new_key}__{func}"
                func = ""

        new_key = colmap.get(new_key, new_key)

        if new_key in colmap and new_key not in toplevel:
            new_key = f"stats__{new_key}__val"

        if func:
            new_key = f"{new_key}__{func}"

        if (
            new_key[0] != "_"
            and "Machine Type" not in new_key
            and "Machine" not in new_key
            and "End Time" not in new_key
            and "endtime" not in new_key
            and "Start Time" not in new_key
            and "starttime" not in new_key
        ):
            name = ""
            op = ""
            value = ""

            if "__" not in new_key:
                # where.append({"name": kw, "op": "eq", "value": kwargs[kw]})
                name = new_key
                op = "eq"
                value = val
            else:
                key1 = "__".join(new_key.split("__")[:-1])
                op = new_key.split("__")[-1]

                if op == "val":
                    op = "eq"
                    key1 += "__val"

                name = key1
                op = op
                value = None
                if op != "exists":
                    value = val
                else:
                    if val:
                        op = "ne"
                    else:
                        op = "ne"

            filter_condition = prepare_filter_condition(name, op, value)

        if filter_condition is not None:
            where_conditions.append(filter_condition)

    if machines:
        if len(machines) > 1:
            source_as_string = str(tuple(machines))
        else:
            source_as_string = f"""('{machines[0]}')"""
        where_conditions.append(f""""Machine" IN {source_as_string}""")

    if machine_type:
        where_conditions.append(f""""Machine Type" IN ('{machine_type}')""")

    where_clause = "\n\tAND ".join([f"{condition}" for condition in where_conditions])

    # Build SQL-query where clause
    # Combine all the clauses to form the final SQL query
    select_clause_str = f"SELECT \n\t{select_clause}"
    from_clause_str = f"\nFROM \n\t{from_clause}"
    where_clause_str = f"\nWHERE \n\t{where_clause}"

    limit_value = kwargs.pop("_limit", 5000)
    offset_value = kwargs.pop("_offset", 0)

    limit_clause_str = f"""\nLIMIT {limit_value}"""
    offset_clause_str = f"""\nOFFSET {offset_value}"""

    if len(order_by_conditions) > 0:
        order_by_clause = ",\n\t ".join(
            [f"{condition}" for condition in order_by_conditions]
        )
        order_by_clause_str = f"\nORDER BY \n\t{order_by_clause}"

    # Build SQL-query
    sql_query_str = f"{select_clause_str}{from_clause_str}{where_clause_str}{order_by_clause_str}{limit_clause_str}{offset_clause_str};"

    # print(f"\n\nDebugInfo: Final SQL Query:\n'''{sql_query_str}'''")

    # Execute the SQL query
    cursor.execute(sql_query_str)

    # Create a DataFrame using the list of rows
    df = pd.DataFrame(
        [
            dict(zip([column[0] for column in cursor.description], row))
            for row in cursor.fetchall()
        ]
    )

    if rename_end_time_col and "Cycle End Time" in df.columns:
        df = df.rename(columns={"Cycle End Time": "End Time"})

    return df
