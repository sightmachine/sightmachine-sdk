import os
import re
import sys
import pyodbc
import logging
import functools
import pandas as pd
import typing as t_
import time
from smsdk import client
from datetime import datetime, timedelta
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    select,
    and_,
    text,
)


log = logging.getLogger(__name__)


def has_duplicates(lst):
    return len(lst) != len(set(lst))


def append_unique_suffix(column_name, seen_columns, all_columns):
    # Convert the column name to lowercase for case insensitivity
    column_name_lower = column_name.lower()

    # If the column name is not already in the list, return it as is
    if column_name_lower not in [name.lower() for name in seen_columns]:
        return column_name

    # Initialize the suffix counter
    suffix_counter = 1

    # Generate a new column name with a unique suffix
    while True:
        new_name = f"{column_name}_{suffix_counter}"
        if new_name.lower() not in [name.lower() for name in all_columns]:
            return new_name
        suffix_counter += 1


def replace_column_names(column_names, column_map):
    replaced_column_names = []
    for column_name in column_names:
        # Check if the column name exists in the column map
        original_column_name = column_map.get(column_name, column_name)
        replaced_column_names.append(original_column_name)
    return replaced_column_names


def replace_duplicate_names(column_names):
    # Check for duplicates
    if has_duplicates(column_names):
        raise ValueError("Input list contains duplicate entities")

    # Convert all strings to lowercase for case-insensitive comparison
    column_names_lowercase = [s.lower() for s in column_names]

    if has_duplicates(column_names_lowercase):
        unique_column_names = []
        original_column_name_map = {}
        seen_columns = set()

        for column in column_names:
            unique_column_name = append_unique_suffix(
                column, seen_columns, column_names
            )

            seen_columns.add(column)
            unique_column_names.append(unique_column_name)

            if len(unique_column_name) != len(column):
                original_column_name_map[unique_column_name] = column

        return unique_column_names, original_column_name_map
    return column_names, {}


def replace_words(input_string, word_map):
    # Create a regular expression pattern to match the words in the map
    pattern = re.compile(r"\b(?:%s)\b" % "|".join(map(re.escape, word_map.keys())))

    # Replace the matched words with their corresponding values from the map
    modified_string = pattern.sub(lambda match: word_map[match.group(0)], input_string)

    return modified_string


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
SQLALCHEMY_OPERATOR_MAPPING = {
    "eq": "__eq__",
    "ne": "__ne__",
    "lt": "__lt__",
    "lte": "__le__",
    "gt": "__gt__",
    "gte": "__ge__",
}


def prepare_filter_condition(table, key_name, key_op, key_val):
    filter_condition = None

    if key_op in SQLALCHEMY_OPERATOR_MAPPING:
        filter_condition = getattr(
            table.columns[key_name], SQLALCHEMY_OPERATOR_MAPPING[key_op]
        )(key_val)
    else:
        # Handle unsupported operators
        print(f"Error: Unsupported operator '{key_op}' in where condition.")

    return filter_condition


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
    machine_table_name = f"sightmachine.cycle_{machine_type}"

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

    try:
        # Create a SQLite in-memory database
        stmt = None
        sql_query_string = ""
        original_column_name_map = {}

        engine = create_engine("sqlite:///:memory:", echo=True)
        metadata = MetaData()

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
                "Machine" if col in {"machine__source"} else col
                for col in select_columns
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
                    colmap.get(col, col)
                    for col in used_names.intersection(available_names)
                ]

            # # Just for debugging
            # select_columns.append("STEAM TO HEAT EXCHANGER SECTION 3 MD")

        select_columns, original_column_name_map = replace_duplicate_names(
            select_columns
        )

        # Table columns
        columns = [Column(column_name, String) for column_name in select_columns]

        # Table
        machine_table = Table(machine_table_name, metadata, *columns)

        # Create the Table & columns
        metadata.create_all(engine)

        # Build SQL-query select clause
        stmt = select(*(machine_table.columns[column] for column in select_columns))

        order_by_filters = []
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

                if order_key.startswith("-"):
                    order_key = order_key[1:]
                    order_by_filters.append(machine_table.columns[order_key].desc())
                else:
                    order_by_filters.append(machine_table.columns[order_key])
        else:
            name = "Cycle End Time"
            order_by_filters.append(machine_table.columns[name].desc())

        # Build SQL-query order-by clause
        stmt = stmt.order_by(*order_by_filters)

        # Replace 'End Time' with 'Cycle End Time' in the keys of the query dictionary
        for key in list(kwargs.keys()):
            if "End Time" in key:
                new_key = key.replace("End Time", "Cycle End Time")
                kwargs[new_key] = kwargs.pop(key)
                rename_end_time_col = True
            if "Start Time" in key:
                new_key = key.replace("Start Time", "Cycle Start Timee")
                kwargs[new_key] = kwargs.pop(key)

        where_filters = []
        etime = datetime.now()
        stime = etime - timedelta(days=1)

        start_key, end_key = get_starttime_endtime_keys(**kwargs)

        starttime = kwargs.pop(start_key, "") if start_key else stime
        name = start_key.split("__")[0]
        op = start_key.split("__")[-1]
        value = starttime.isoformat()

        filter_condition = None
        filter_condition = prepare_filter_condition(machine_table, name, op, value)

        if filter_condition is not None:
            where_filters.append(filter_condition)

        endtime = kwargs.pop(end_key, "") if end_key else etime
        name = end_key.split("__")[0]
        op = end_key.split("__")[-1]
        value = endtime.isoformat()

        filter_condition = None
        filter_condition = prepare_filter_condition(machine_table, name, op, value)

        if filter_condition is not None:
            where_filters.append(filter_condition)

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

                filter_condition = prepare_filter_condition(
                    machine_table, name, op, value
                )

            if filter_condition is not None:
                where_filters.append(filter_condition)

        # Include machine source and machine type in the WHERE clause
        machine_source = kwargs.pop("Machine", "")
        machine_type = kwargs.pop("Machine Type", "")

        if machine_source:
            if isinstance(machine_source, list):
                source_as_string = str(tuple(machine_source))
            else:
                source_as_string = f"""('{machine_source}')"""
            where_filters.append(
                text(f'"{machine_table_name}"."Machine" IN :machine_source').bindparams(
                    machine_source=source_as_string
                )
            )

        if machine_type:
            machine_type = f"""('{machine_type}')"""
            where_filters.append(
                text(
                    f'"{machine_table_name}"."Machine Type" IN :machine_type'
                ).bindparams(machine_type=machine_type)
            )

        # Build SQL-query where clause
        if len(where_filters):
            stmt = stmt.where(and_(*where_filters))

        limit_value = kwargs.pop("_limit", 5000)
        offset_value = kwargs.pop("_offset", 0)

        # Build SQL-query LIMIT and OFFSET clauses
        stmt = stmt.limit(limit_value).offset(offset_value)

        compiled_stmt = stmt.compile()

        # Access the SQL string with bindings
        sql_query_string = compiled_stmt.string

        # Access the binding parameters mapping
        binding_mapping = compiled_stmt.params

        # Replace bindings with actual values in the SQL string
        for key, value in binding_mapping.items():
            # Check if the value is a string and not enclosed in parentheses
            if isinstance(value, str) and not (
                value.startswith("(") and value.endswith(")")
            ):
                # Enclose the string value in single quotes
                value = f"'{value}'"

            # Replace each occurrence of the binding with its actual value in the SQL string
            sql_query_string = sql_query_string.replace(f":{key}", str(value))

            # Remove double quotes around the table name
            sql_query_string = sql_query_string.replace(
                f'"{machine_table_name}"', machine_table_name
            )

        if len(original_column_name_map):
            sql_query_string = replace_words(sql_query_string, original_column_name_map)
    except Exception as e:
        print(f"Error: Failed to generate the SQL query. {str(e)}")

    # print(f"\n\nDebugInfo: sql string - '''\n{sql_query_string}\n'''\n\n")

    # Execute the SQL query
    cursor.execute(sql_query_string)

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
