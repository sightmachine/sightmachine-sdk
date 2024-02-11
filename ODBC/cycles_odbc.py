import functools

import numpy as np
import pandas as pd

import sys
import pyodbc

import typing as t_
from datetime import datetime, timedelta
import logging
from smsdk import client
from smsdk import const
from sqlalchemy import create_engine, MetaData, Table, Column, String, select, and_

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


def connect_to_db():
    conn = None
    cursor = None

    db_params = {
        "driver": "{PostgreSQL Unicode}",
        "server": f"{const.TENANT}.sightmachine.io",
        "port": "5432",
        "database": "tenant_storage",
        "uid": const.API_KEY,
        "pwd": const.API_SECRETE,
    }

    # Create a connection string for pyodbc
    conn_str = (
        f"DRIVER={db_params['driver']};"
        f"SERVER={db_params['server']};"
        f"PORT={db_params['port']};"
        f"DATABASE={db_params['database']};"
        f"UID={db_params['uid']};"
        f"PWD={db_params['pwd']};"
        f"SSLmode=require;"
    )

    try:
        # Establish a connection
        conn = pyodbc.connect(conn_str)

        # Create a cursor from the connection
        cursor = conn.cursor()

    except Exception as ex:
        print(f"Error:: {str(ex)} :: Connection to the DB failed")
        sys.exit(1)

    return (conn, cursor)


def disconnect(conn, cursor):
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


def display_query_machine_titles(
    machine_schema: pd.DataFrame, query: t_.Dict[str, t_.Any]
) -> t_.Dict[str, t_.Any]:
    """
    Given a query for cycles that uses internal Sight Machine names, convert the machines into UI friendly tag/field names
    :param query: Dict kwargs passed as part of a query to the API
    :return: dict
    """

    colmap = {row[1]["name"]: row[1]["display"] for row in machine_schema.iterrows()}
    toplevel = {
        "endtime": "End Time",
        "starttime": "Start Time",
        "machine__source": "Machine",
        "total": "Cycle Time (Net)",
        "record_time": "Cycle Time (Gross)",
        "shift": "Shift",
        "output": "Output",
    }
    colmap.update(toplevel)

    translated_query = {}
    for key, val in query.items():
        # Special handling for _order_by since the stat titles are in a list
        if key == "_order_by":
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

            # For performance, currently only support order by time, machine
            if not val in ["Cycle End Time", "Cycle Start Time", "Machine"]:
                log.warn(
                    "Only ordering by 'Start Time', 'End Time' and 'Machine' source currently supported."
                )
                continue

            val = f"{prefix}{val}"

        # Special handling for _only
        elif key == "_only":
            # To simplify the logic, always treat as a list of _only items
            if isinstance(val, str):
                val = [val]

            val = [colmap.get(col, col) for col in val]

        # for all other params
        else:
            func = ""
            if "__" in key:
                parts = key.split("__")
                key = "__".join(parts[:-1])
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
                    key = f"{key}__{func}"
                    func = ""

            key = colmap.get(key, key)
            if key in colmap and key not in toplevel:
                key = f"stats__{key}__val"

            if func:
                key = f"{key}__{func}"

        translated_query[key] = val

    return translated_query


def clean_query_machine_names(
    client: client.Client, query: t_.Dict[str, t_.Union[str, t_.List]]
) -> t_.Dict[str, t_.Union[str, t_.List]]:
    """
    Given a query using the UI friendly machine names, convert them into the Sight Machine expected internal names
    :param query: Dict kwargs passed as part of a query to the API
    :return: dict
    """
    query = query.copy()

    machine_key = "Machine" if "Machine" in query else "Machine__in"

    query_params = {
        "_only": ["source", "source_clean", "source_type"],
        "_order_by": "source_clean",
    }
    mach_names = client.get_machines(**query_params)
    machmap = {
        mach[1]["source_clean"]: mach[1]["source"] for mach in mach_names.iterrows()
    }

    machines = query[machine_key]

    if isinstance(machines, str):
        query[machine_key] = machmap.get(machines, machines)
    else:
        query[machine_key] = [machmap.get(mach, mach) for mach in machines]

    return query


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


def prepare_query(**kwargs: t_.Any) -> t_.Dict[str, t_.Any]:
    machine_type = kwargs.get("Machine Type", "")
    if machine_type.startswith("'") and machine_type.endswith("'"):
        machine_type = machine_type[1:-1]

    new_kwargs = {}
    etime = datetime.now()
    stime = etime - timedelta(days=1)
    new_kwargs["asset_selection"] = {
        "Machine": kwargs.get("Machine", ""),
        "Machine Type": machine_type,
    }

    start_key, end_key = get_starttime_endtime_keys(**kwargs)

    where = []
    starttime = kwargs.get(start_key, "") if start_key else stime
    where.append(
        {
            "name": start_key.split("__")[0],
            "op": start_key.split("__")[-1],
            "value": starttime.isoformat(),
        }
    )

    endtime = kwargs.get(end_key, "") if end_key else etime
    where.append(
        {
            "name": end_key.split("__")[0],
            "op": end_key.split("__")[-1],
            "value": endtime.isoformat(),
        }
    )

    for kw in kwargs:
        if (
            kw[0] != "_"
            and "Machine Type" not in kw
            and "Machine" not in kw
            and "End Time" not in kw
            and "endtime" not in kw
            and "Start Time" not in kw
            and "starttime" not in kw
        ):
            if "__" not in kw:
                where.append({"name": kw, "op": "eq", "value": kwargs[kw]})
            else:
                key = "__".join(kw.split("__")[:-1])
                op = kw.split("__")[-1]

                if op == "val":
                    op = "eq"
                    key += "__val"

                if op != "exists":
                    where.append({"name": key, "op": op, "value": kwargs[kw]})
                else:
                    if kwargs[kw]:
                        where.append({"name": key, "op": "ne", "value": None})
                    else:
                        where.append({"name": key, "op": "eq", "value": None})

    new_kwargs["select"] = [{"name": i} for i in kwargs["_only"]]
    new_kwargs["offset"] = kwargs.get("_offset", 0)
    new_kwargs["limit"] = kwargs.get("_limit", np.Inf)
    new_kwargs["where"] = where

    if "_order_by" in kwargs:
        order_key = kwargs["_order_by"].replace("_epoch", "")
        if order_key.startswith("-"):
            order_type = "desc"
            order_key = order_key[1:]
        else:
            order_type = "asc"
        new_kwargs["order_by"] = [{"name": order_key, "order": order_type}]
    else:
        new_kwargs["order_by"] = [
            {"name": "Cycle End Time", "order": "desc"},
            {"name": "_id", "order": "desc"},
        ]

    return new_kwargs


# Define a dictionary to map comparison operators
OPERATOR_MAPPING = {
    "gt": ">",
    "lt": "<",
    "gte": ">=",
    "lte": "<=",
    "ne": "<>",
    "eq": "=",
}


def generate_sqlalchemy_query_string(get_type, machine_schema, **query_dict):
    asset_selection = query_dict["asset_selection"]
    select_columns = [item["name"] for item in query_dict["select"]]
    where_conditions = query_dict.get("where", [])
    order_by_conditions = query_dict.get("order_by", [])
    limit_value = query_dict.get("limit", 10)
    offset_value = query_dict.get("offset", 0)

    # Create a SQLite in-memory database
    engine = create_engine("sqlite:///:memory:", echo=True)
    metadata = MetaData()

    # Define a table dynamically based on the columns present in the asset selection
    columns = []
    for column_name in select_columns:
        columns.append(Column(column_name, String))

    # Define the table
    machine_table = Table("machine_table", metadata, *columns)

    # Create the table
    metadata.create_all(engine)

    # Populate the table with data (in this case, no data is inserted)

    # Build the query
    stmt = select([machine_table.columns[column] for column in select_columns])

    # Add WHERE conditions
    where_filters = []
    for condition in where_conditions:
        name = condition["name"]
        op = condition["op"]
        value = condition["value"]
        if op == "in":
            where_filters.append(machine_table.columns[name].in_(value))
        else:
            where_filters.append(getattr(machine_table.columns[name], op)(value))

    if where_filters:
        stmt = stmt.where(and_(*where_filters))

    # Add ORDER BY conditions
    order_by_filters = []
    for order_by in order_by_conditions:
        name = order_by["name"]
        order = order_by["order"]
        if order == "desc":
            order_by_filters.append(machine_table.columns[name].desc())
        else:
            order_by_filters.append(machine_table.columns[name])

    if order_by_filters:
        stmt = stmt.order_by(*order_by_filters)

    # Add LIMIT and OFFSET clauses
    stmt = stmt.limit(limit_value).offset(offset_value)

    # Print the generated SQL
    print(f"\n\n\nDebugInfo:: stmt - {stmt}")


def generate_sql_query_string(get_type, machine_schema, **query_dict):
    select_clause_str = ""
    from_clause_str = ""
    where_clause_str = ""
    order_by_clause_str = ""
    limit_clause_str = ""
    offset_clause_str = ""

    # Extract the 'select' part of the query
    select_columns = [item["name"] for item in query_dict.get("select", [])]

    # Extract 'asset_selection' information for the FROM clause
    asset_selection = query_dict.get("asset_selection", {})
    machine_source = asset_selection.get("Machine", None)
    machine_type = asset_selection.get("Machine Type", None)

    # Generate the SELECT clause based on the 'display' names in the query
    select_clause = ",\n\t".join([f'"{column}"' for column in select_columns])

    # Generate the WHERE clause based on the 'where' conditions in the query
    where_conditions = []
    if "where" in query_dict:
        for condition in query_dict["where"]:
            name = condition["name"]
            op = condition.get("op", None)
            value = condition.get("value", None)

            if op and value is not None:
                # Replace operation with the corresponding symbol
                op = OPERATOR_MAPPING.get(op, op)

                # Add the condition to the list
                where_conditions.append(f""""{name}" {op} '{value}'""")

    # Include machine source and machine type in the WHERE clause
    if machine_source:
        if isinstance(machine_source, list):
            source_as_string = str(tuple(machine_source))
        else:
            source_as_string = f"('{machine_source}')"
        where_conditions.append(f""""Machine" IN {source_as_string}""")
    if machine_type:
        where_conditions.append(f""""Machine Type" IN ('{machine_type}')""")

    where_clause = "\n\tAND ".join([f"{condition}" for condition in where_conditions])

    # Generate the ORDER BY clause based on the 'order_by' conditions in the query
    order_by_conditions = []
    if "order_by" in query_dict:
        for order_by in query_dict["order_by"]:
            name = order_by["name"]
            order_by_conditions.append(f'"{name}" {order_by["order"]}')

    from_clause = f"sightmachine.{get_type}_{machine_type}"

    # Combine all the clauses to form the final SQL query
    select_clause_str = f"SELECT \n\t{select_clause}"
    from_clause_str = f"\nFROM \n\t{from_clause}"
    where_clause_str = f"\nWHERE \n\t{where_clause}"

    if "offset" in query_dict:
        offset_clause_str = f"""\nOFFSET {query_dict["offset"]}"""

    if "limit" in query_dict:
        limit_value = query_dict["limit"]
        if not isinstance(limit_value, int):
            # Assign a default value of 5000 if the limit value is not an integer
            # limit_value = 87000,  # number of seconds in a day is 86400
            limit_value = sys.maxsize
        limit_clause_str = f"""\nLIMIT {limit_value}"""

    if len(order_by_conditions) > 0:
        order_by_clause = ",\n\t ".join(
            [f"{condition}" for condition in order_by_conditions]
        )
        order_by_clause_str = f"\nORDER BY \n\t{order_by_clause}"

    sql_query = f"{select_clause_str}{from_clause_str}{where_clause_str}{order_by_clause_str}{limit_clause_str}{offset_clause_str};"

    return sql_query


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

    # print(f"\n\nDebugInfo:: marke1 - args: '{kwargs}'\n\n")

    machine = kwargs.get("machine__source", kwargs.get("Machine"))
    if not machine:
        # Possible that it is a machine__in.  If so, base on first machine
        machine = kwargs.get("machine__source__in", kwargs.get("Machine__in"))
        kwargs["Machine"] = machine

    if isinstance(machine, str):
        machine_type, machine_schema = client.get_machine_schema(
            machine, return_mtype=True
        )
    else:  # it is a list of machines, work with first name in list
        machine_type, machine_schema = client.get_machine_schema(
            machine[0], return_mtype=True
        )

    if not "_only" in kwargs:
        log_or_print("_only not specified. Selecting first 50 fields.", log, "info")
        only_names = machine_schema["display"].tolist()[:50]
        kwargs["_only"] = only_names
    else:
        if all(
            i not in {"End Time", "endtime", "Cycle End Time"} for i in kwargs["_only"]
        ):
            log_or_print("Adding 'Cycle End Time' to _only", log, "info")
            kwargs["_only"].insert(0, "Cycle End Time")

        if all(i not in {"Machine", "machine__source"} for i in kwargs["_only"]):
            log_or_print("Adding 'Machine' to _only", log, "info")
            kwargs["_only"].insert(0, "Machine")

        # # Add '_id' to query columns if not present.
        # if "_id" not in [i for i in kwargs["_only"]]:
        #     kwargs["_only"].append("_id")

    # Replace  'End Time' &  'endtime' with 'Cycle End Time' if they are present in '_only' value list
    if "_only" in kwargs:
        if "End Time" in kwargs["_only"]:
            kwargs["_only"] = [
                col.replace("End Time", "Cycle End Time") for col in kwargs["_only"]
            ]
            rename_end_time_col = True
        elif "endtime" in kwargs["_only"]:
            kwargs["_only"] = [
                col.replace("endtime", "Cycle End Time") for col in kwargs["_only"]
            ]
            rename_end_time_col = True

    # Replace 'End Time' with 'Cycle End Time' in the keys of the query dictionary
    for key in list(kwargs.keys()):
        if "End Time" in key:
            new_key = key.replace("End Time", "Cycle End Time")
            kwargs[new_key] = kwargs.pop(key)
            rename_end_time_col = True
        if "Start Time" in key:
            new_key = key.replace("Start Time", "Cycle Start Timee")
            kwargs[new_key] = kwargs.pop(key)

    if kwargs["_only"] == "*":
        kwargs.pop("_only")

    if "_only" in kwargs:
        available_names = set(
            machine_schema["name"].to_list()
            + machine_schema["display"].to_list()
            + [
                "record_time",
                "endtime",
                "total",
                "machine__source",
                "starttime",
                "output",
                "shift",
            ]
            + [
                "Cycle Time (Gross)",
                "End Time",
                "Cycle Time (Net)",
                "Machine",
                "Start Time",
                "Output",
                "Shift",
            ]
        )
        used_names = set(kwargs["_only"])
        different_names = used_names.difference(available_names)

        if len(different_names) > 0:
            log_or_print(
                f'Dropping invalid column names: {", ".join(different_names)}.',
                log,
                "info",
            )
            kwargs["_only"] = used_names.intersection(available_names)

    kwargs.update({"Machine Type": machine_type})

    # Add '_id' to query columns if not present.
    if "_id" not in [i for i in kwargs["_only"]]:
        kwargs["_only"].append("_id")

    if clean_strings_in:
        # print(f"\n\nDebugInfo:: marke2 - args: '{kwargs}'\n\n")
        kwargs = display_query_machine_titles(machine_schema, kwargs)
        # print(f"\n\nDebugInfo:: marke3 - args: '{kwargs}'\n\n")
        kwargs = clean_query_machine_names(client, kwargs)
        # print(f"\n\nDebugInfo:: marke4 - args: '{kwargs}'\n\n")

    kwargs = prepare_query(**kwargs)

    print(f"\n\nDebugInfo:: marke5 - args: '{kwargs}'\n\n")

    sql_query_str = generate_sql_query_string("cycle", machine_schema, **kwargs)
    generate_sqlalchemy_query_string("cycle", machine_schema, **kwargs)

    print(f"\n\nDebugInfo: sql string - '''\n{sql_query_str}\n'''\n\n")

    # Execute the SQL query
    cursor.execute(sql_query_str)

    # Create a DataFrame using the list of rows
    df = pd.DataFrame(
        [
            dict(zip([column[0] for column in cursor.description], row))
            for row in cursor.fetchall()
        ]
    )

    # Set the index of the DataFrame to the '_id' column
    if "_id" in df.columns:
        df.set_index("_id", inplace=True)

    if rename_end_time_col and "Cycle End Time" in df.columns:
        df = df.rename(columns={"Cycle End Time": "End Time"})

    return df
