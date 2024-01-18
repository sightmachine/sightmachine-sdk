import functools

import numpy as np
import pandas as pd

import sys
import pyodbc

from datetime import datetime, timedelta
import logging
from smsdk import client

log = logging.getLogger(__name__)


MACHINE_TYPE_TO_TABLE_VIEW_NAME = {
    "Lasercut": "cycle_lasercut",
    "PickAndPlace": "cycle_lasercut",
    "Pick & Place": "cycle_lasercut",
    "Diecast": "cycle_diecast",
    "Fusion": "cycle_fusion",
}


def get_cursor():
    conn = None
    cursor = None

    db_params = {
        "driver": "{PostgreSQL Unicode}",
        "server": "demo-sdk-test.sightmachine.io",
        "port": "5432",
        "database": "tenant_storage",
        "uid": "5a73aa5a-1962-4df9-b56e-4a59462f0f00",
        "pwd": "sma_FajgH3VbPu68gwy0PzccvhyGRyy1a8CCHhhvy6ooeg1O_",
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


def close_connection(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def validate_input(func):
    """This decorator can be used to validate input schema with some conditions,
    or can implement jsonschema validator in later versions if required"""

    @functools.wraps(func)
    def validate(*args, **kwargs):
        exceptional_keys = ["_only"]
        for key in kwargs:
            if key in exceptional_keys:
                continue
            if isinstance(kwargs[key], list):
                if not (key.endswith("__in") or key.endswith("__nin")):
                    msg = f"Key <{key}> should have '__in' or '__nin' in it if datatype is list"
                    raise ValueError(msg)
        return func(*args, **kwargs)

    return validate


def display_query_machine_titles(machine_schema, query):
    """
    Given a query for cycles that uses internal Sight Machine names, convert the machines into UI friendly tag/field names

    :param query: Dict kwargs passed as part of a query to the API

    :return: dict
    """

    # First need to find the machine name
    machine = query.get("machine__source", query.get("Machine"))
    if isinstance(machine, list):
        # Possible that it is a machine__in.  If so, base on the first machine
        machine = query.get("machine__source__in", query.get("Machine__in"))
        machine = machine[0]

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
                val = "endtime"
            if val == "Start Time":
                val = "starttime"
            val = colmap.get(val, val)

            # For performance, currently only support order by time, machine
            if not val in ["endtime_epoch", "starttime_epoch", "Machine"]:
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


def clean_query_machine_names(client, query):
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


def get_starttime_endtime_keys(**kwargs):
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


def prepare_query(**kwargs):
    # Special handling for EF type names
    machine = kwargs.get("Machine", "")

    if machine[0] == "'":
        machine = machine[1:-1]

    machine_type = kwargs.get("Machine Type", "")
    if machine_type[0] == "'":
        machine_type = machine_type[1:-1]

    new_kwargs = {}
    etime = datetime.now()
    stime = etime - timedelta(days=1)
    new_kwargs["asset_selection"] = {
        "Machine": machine,
        "Machine Type": machine_type,
    }

    start_key, end_key = get_starttime_endtime_keys(**kwargs)

    # https://37-60546292-gh.circle-artifacts.com/0/build/html/web_api/v1/datatab/index.html#get--v1-datatab-cycle
    where = []
    if start_key:
        starttime = kwargs.get(start_key, "") if start_key else stime
        where.append(
            {
                "name": start_key.split("__")[0],
                "op": start_key.split("__")[-1],
                "value": starttime.isoformat(),
            }
        )

    if end_key:
        endtime = kwargs.get(end_key, "") if end_key else stime
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

    if kwargs.get("_order_by", ""):
        order_key = kwargs["_order_by"].replace("_epoch", "")
        if order_key.startswith("-"):
            order_type = "desc"
            order_key = order_key[1:]
        else:
            order_type = "asc"
        new_kwargs["order_by"] = [{"name": order_key, "order": order_type}]

    return new_kwargs


def generate_sql_query(machine_schema, **query_dict):
    # Extract the 'select' part of the query
    select_columns = [item["name"] for item in query_dict.get("select", [])]

    # Extract 'asset_selection' information for the FROM clause
    asset_selection = query_dict.get("asset_selection", {})
    machine_source = asset_selection.get("Machine", None)
    machine_type = asset_selection.get("Machine Type", None)

    # Generate the SELECT clause based on the 'display' names in the query
    select_clause = ",\n  ".join(
        [f'"{column}"' for column in select_columns]
    )

    # Generate the WHERE clause based on the 'where' conditions in the query
    where_conditions = []
    if "where" in query_dict:
        for condition in query_dict["where"]:
            name = condition["name"]
            op = condition.get("op", None)
            value = condition.get("value", None)

            if op and value is not None:
                # Replace operation with the corresponding symbol
                if op == "gt":
                    op = ">"
                elif op == "lt":
                    op = "<"
                elif op == "gte":
                    op = ">="
                elif op == "lte":
                    op = "<="
                elif op == "ne":
                    op = "<>"
                elif op == "eq":
                    op = "="
                # Add the condition to the list
                where_conditions.append(f""""{name}" {op} '{value}'""")

    # Include machine source and machine type in the WHERE clause
    if machine_source:
        where_conditions.append(f""""Machine" IN ('{machine_source}')""")
    if machine_type:
        where_conditions.append(f""""Machine Type" IN ('{machine_type}')""")

    where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""

    # Generate the ORDER BY clause based on the 'order_by' conditions in the query
    order_by_clause = ""
    if "order_by" in query_dict:
        order_by_conditions = []
        for order_by in query_dict["order_by"]:
            name = order_by["name"]
            order_by_conditions.append(f'"{name}" {order_by["order"]}')
        order_by_clause = "ORDER BY " + ", ".join(order_by_conditions)

    # Determine the table name based on the machine type
    from_clause = "sightmachine."
    from_clause += MACHINE_TYPE_TO_TABLE_VIEW_NAME.get(
        machine_type, "default_table_name"
    )  # Replace with a default table name

    # Combine all the clauses to form the final SQL query
    sql_query = f"""
    SELECT
    {select_clause}
    FROM
    {from_clause}
    {where_clause}
    {order_by_clause}
    LIMIT {query_dict["limit"]} OFFSET {query_dict["offset"]};
    """

    return sql_query


@validate_input
def get_cycles(
    cursor,
    client,
    normalize=True,
    clean_strings_in=True,
    clean_strings_out=True,
    *args,
    **kwargs,
):
    # When processing in batch
    if args and (not kwargs):
        kwargs = args[0]

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

    if not "_limit" in kwargs:
        print("_limit not specified.  Maximum of 5000 rows will be returned.")

    if not "_only" in kwargs:
        print("_only not specified.  Selecting first 50 fields.")
        only_names = machine_schema["display"].tolist()[:50]
        kwargs["_only"] = only_names
    else:
        if all(
            i not in {"End Time", "endtime", "Cycle End Time"} for i in kwargs["_only"]
        ):
            print("Adding 'Cycle End Time' to _only")
            kwargs["_only"].insert(0, "Cycle End Time")

        if all(i not in {"Machine", "machine__source"} for i in kwargs["_only"]):
            print("Adding 'Machine' to _only")
            kwargs["_only"].insert(0, "Machine")

    # Replace 'End Time' with 'Cycle End Time' in the keys of the query dictionary
    for key in list(kwargs.keys()):
        if "End Time" in key:
            new_key = key.replace("End Time", "Cycle End Time")
            kwargs[new_key] = kwargs.pop(key)
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
            print(f'Dropping invalid column names: {", ".join(different_names)}.')
            kwargs["_only"] = used_names.intersection(available_names)

    kwargs.update({"Machine Type": machine_type})

    if clean_strings_in:
        kwargs = display_query_machine_titles(machine_schema, kwargs)
        kwargs = clean_query_machine_names(client, kwargs)


    kwargs = prepare_query(**kwargs)

    sql_query = generate_sql_query(machine_schema, **kwargs)

    # Execute the SQL query
    cursor.execute(sql_query)

    # Create a DataFrame using the list of rows
    df = pd.DataFrame(
        [
            dict(zip([column[0] for column in cursor.description], row))
            for row in cursor.fetchall()
        ]
    )

    return df
