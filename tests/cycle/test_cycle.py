import pandas as pd
from datetime import datetime
from tests.conftest import TENANT
from smsdk.smsdk_entities.cycle.cycleV1 import Cycle
from tests.cycle.cycle_data import JSON_MACHINE_CYCLE_50
import unittest
from smsdk.custom_exception.errors import NotFound

import ODBC.cycles_odbc as odbc

# from ODBC.odbc_helper import Cycles as odbc
import time
import typing as t_


# Define all the constants used in the test
MACHINE_TYPE = "Lasercut"
MACHINE_INDEX = 5
START_DATETIME = datetime(2023, 4, 1)
END_DATETIME = datetime(2023, 4, 2)
NUM_ROWS = 500
URL_V1 = "/v1/datatab/cycle"


def test_get_utilities(get_session):
    cycle = Cycle(get_session, TENANT)

    # Run
    all_utilites = cycle.get_utilities(get_session, URL_V1)

    expected_list = ["get_utilities", "get_cycles"]

    assert len(all_utilites) == len(expected_list)
    assert all([a == b for a, b in zip(all_utilites, expected_list)])


def test_get_cycles_monkeypatch(monkeypatch, get_session):
    # Setup
    def mockapi(self, session, endpoint, **kwargs):
        if endpoint.startswith(URL_V1):
            return pd.DataFrame(JSON_MACHINE_CYCLE_50)
        return pd.DataFrame()

    monkeypatch.setattr(Cycle, "get_cycles", mockapi)

    dt = Cycle(get_session, TENANT)

    # Run
    df = dt.get_cycles(get_session, URL_V1)

    assert df.shape == (50, 29)


def test_get_cycles(get_client):
    types = get_client.get_machine_type_names()
    machines = get_client.get_machine_names(source_type=types[0])
    print(f"\nDebugInfo:: types - '{types}'")
    print(f"DebugInfo:: machines - '{machines}'")
    machine = machines[0]
    columns = get_client.get_machine_schema(machine)["display"].to_list()

    query = {
        "Machine": machines[0],
        "End Time__gte": datetime(2024, 1, 14),
        "End Time__lt": datetime(2024, 1, 21),
        "_only": columns[:5],
        "_limit": 50,
    }

    df1 = get_client.get_cycles(**query)

    print(df1.head())
    print()
    print()

    query = {
        "Machine__in": machines[0:5],
        "End Time__gte": datetime(2024, 1, 14),
        "End Time__lt": datetime(2024, 1, 21),
        "_only": columns[:5],
        "_limit": 50,
    }

    df2 = get_client.get_cycles(**query)

    print(df2.head())
    print()
    print()


def test_get_cycles_odbc(get_client):
    types = get_client.get_machine_type_names()
    machines = get_client.get_machine_names(source_type=types[0])

    # print(f"\nDebugInfo:: types - '{types}'")
    # print(f"\nDebugInfo:: machines - '{machines}'")

    machine = machines[0]
    columns = get_client.get_machine_schema(machine)["display"].to_list()

    conn, cursor = odbc.connect_to_db()

    query = {
        "Machine": machines[0],
        # "Machine__in": machines[0:5],
        "End Time__gte": datetime(2024, 1, 14),
        "End Time__lt": datetime(2024, 1, 21),
        "_only": columns[:15],
        "_limit": 11,
    }

    df1 = odbc.get_cycles(cursor, get_client, **query)

    print(df1.head())
    print()
    print()

    query = {
        "Machine__in": machines[0:5],
        "End Time__gte": datetime(2024, 1, 14),
        "End Time__lt": datetime(2024, 1, 21),
        "_only": columns[:5],
        "_limit": 11,
    }

    df2 = odbc.get_cycles(cursor, get_client, **query)

    odbc.disconnect(conn, cursor)

    print(df2.head())
    print()
    print()


def test_get_cycles_odbc_latency(get_client):
    types = get_client.get_machine_type_names()
    machines = get_client.get_machine_names(source_type=types[0])
    machine = machines[0]
    columns = get_client.get_machine_schema(machine)["display"].to_list()

    print(f"\nDebugInfo:: types - '{types}'")
    print(f"DebugInfo:: machines - '{machines}'")

    query = {
        # "Machine": machines[0],
        "Machine__in": machines[0:5],
        "End Time__gte": datetime(2024, 1, 14),
        "End Time__lt": datetime(2024, 1, 21),
        # "_only": ["Cycle End Time", "5th Dryer Section Speed FPM", "Machine"],
        "_only": columns[:5],
        "_limit": 7,  # number of seconds in a day is 86400
    }

    # # Measure the time taken by the API call
    # start_sdk_api_time_ns = time.time_ns()
    # df1 = get_client.get_cycles(**query)
    # time.time_ns()

    # sdk_api_elapsed_time_ms = (end_sdk_api_time_ns - start_sdk_api_time_ns) / 1e6
    # print(
    #     f"\nDebugInfo: Time taken by SDK 'get_cycles': {sdk_api_elapsed_time_ms:.2f} milliseconds"
    # )

    for i in range(1):
        df2 = None
        start_odbc_api_time_ns = time.time_ns()

        conn, cursor = odbc.connect_to_db()
        df2 = odbc.get_cycles(cursor, get_client, **query)
        odbc.disconnect(conn, cursor)

        # Calculate the time taken
        end_odbc_time_ns = time.time_ns()

        odbc_elapsed_time_ms = (end_odbc_time_ns - start_odbc_api_time_ns) / 1e6

        print(
            f"\nDebugInfo[iter-{i}]: Time taken by ODBC 'get_cycles': {odbc_elapsed_time_ms:.2f} milliseconds"
        )

        # comparison = df1.head(5).equals(df1.head(5))

        # if comparison:
        #     print(f"DebugInfo[100][iter-{i}]:: Data matching")
        # else:
        #     print(f"\n\nDebugInfo[103][iter-{i}]:: columsn of df1 - {df1.columns}")
        #     print(f"DebugInfo[101][iter-{i}]:: First two rows of df1...\n{df1.head(4)}")

        #     print(f"\n\nDebugInfo[104][iter-{i}]:: columsn of df2 - {df2.columns}")
        #     print(f"DebugInfo[102][iter-{i}]::First two rows of df2..\n{df2.head(4)}\n")

        # print(f"{df2.shape}")

    # # Assert that the two DataFrames are equal
    # assert df1.shape == (NUM_ROWS, len(columns))
    # assert df2.shape == (NUM_ROWS, len(columns))


def test_get_cycles_with_fake_source(get_client):
    machines = get_client.get_machine_names(source_type=MACHINE_TYPE)
    machine = machines[MACHINE_INDEX]
    columns = get_client.get_machine_schema(machine)["display"].to_list()

    query = {
        "Machine": "fake_machine",
        "End Time__gte": START_DATETIME,
        "End Time__lte": END_DATETIME,
        "_order_by": "-End Time",
        "_limit": NUM_ROWS,
        "_only": columns,
    }
    # NotFound is expected because of machine that does not exist.
    with unittest.TestCase().assertRaises(NotFound) as context:
        df = get_client.get_cycles(**query)


def test_get_cycles_machine_tag(get_client):
    machines = get_client.get_machine_names(source_type=MACHINE_TYPE)
    machine = machines[MACHINE_INDEX]
    columns = get_client.get_machine_schema(machine)["display"].to_list()

    select_columns = [
        # "Machine",
        "Cycle Start Time",
        "Cycle End Time",
        "Production Day",
        "Cycle Time (Net)",
        "Cycle Time (Gross)",
    ]

    col = select_columns.copy()

    query = {
        "Machine": machine,
        "End Time__gte": START_DATETIME,
        "End Time__lte": END_DATETIME,
        "_order_by": "-End Time",
        "_limit": NUM_ROWS,
        "_only": col,
    }

    df = get_client.get_cycles(**query)

    assert df.shape == (NUM_ROWS, len(select_columns) + 1)

    select_columns = [
        "machine__source",
        "Cycle Start Time",
        "Cycle End Time",
        "Production Day",
        "Cycle Time (Net)",
        "Cycle Time (Gross)",
    ]

    col = select_columns.copy()

    query = {
        "Machine": machine,
        "End Time__gte": START_DATETIME,
        "End Time__lte": END_DATETIME,
        "_order_by": "-End Time",
        "_limit": NUM_ROWS,
        "_only": col,
    }

    df = get_client.get_cycles(**query)

    assert df.shape == (NUM_ROWS, len(select_columns))


def test_get_cycles_starttime_tag(get_client):
    machines = get_client.get_machine_names(source_type=MACHINE_TYPE)
    machine = machines[MACHINE_INDEX]
    columns = get_client.get_machine_schema(machine)["display"].to_list()

    select_columns = [
        "Machine",
        "Cycle End Time",
        "Production Day",
        "Cycle Time (Net)",
        "Cycle Time (Gross)",
    ]

    col = select_columns.copy()

    query = {
        "Machine": machine,
        "End Time__gte": START_DATETIME,
        "End Time__lte": END_DATETIME,
        "_order_by": "-End Time",
        "_limit": NUM_ROWS,
        "_only": col,
    }

    df = get_client.get_cycles(**query)

    assert df.shape == (NUM_ROWS, len(select_columns))

    select_columns = [
        "Machine",
        "starttime",
        "Cycle End Time",
        "Production Day",
        "Cycle Time (Net)",
        "Cycle Time (Gross)",
    ]

    col = select_columns.copy()

    query = {
        "Machine": machine,
        "End Time__gte": START_DATETIME,
        "End Time__lte": END_DATETIME,
        "_order_by": "-End Time",
        "_limit": NUM_ROWS,
        "_only": col,
    }

    df = get_client.get_cycles(**query)

    assert df.shape == (NUM_ROWS, len(select_columns))

    select_columns = [
        "Machine",
        "Start Time",
        "Cycle End Time",
        "Production Day",
        "Cycle Time (Net)",
        "Cycle Time (Gross)",
    ]

    col = select_columns.copy()

    query = {
        "Machine": machine,
        "End Time__gte": START_DATETIME,
        "End Time__lte": END_DATETIME,
        "_order_by": "-End Time",
        "_limit": NUM_ROWS,
        "_only": col,
    }

    df = get_client.get_cycles(**query)

    assert df.shape == (NUM_ROWS, len(select_columns))


def test_get_cycles_endtime_tag(get_client):
    machines = get_client.get_machine_names(source_type=MACHINE_TYPE)
    machine = machines[MACHINE_INDEX]
    columns = get_client.get_machine_schema(machine)["display"].to_list()

    select_columns = [
        "Machine",
        "Cycle Start Time",
        # "Cycle End Time",
        "Production Day",
        "Cycle Time (Net)",
        "Cycle Time (Gross)",
    ]

    col = select_columns.copy()

    query = {
        "Machine": machine,
        "End Time__gte": START_DATETIME,
        "End Time__lte": END_DATETIME,
        "_order_by": "-End Time",
        "_limit": NUM_ROWS,
        "_only": col,
    }

    df = get_client.get_cycles(**query)

    assert df.shape == (NUM_ROWS, len(select_columns) + 1)

    select_columns = [
        "Machine",
        "Cycle Start Time",
        "endtime",
        "Production Day",
        "Cycle Time (Net)",
        "Cycle Time (Gross)",
    ]

    col = select_columns.copy()

    query = {
        "Machine": machine,
        "End Time__gte": START_DATETIME,
        "End Time__lte": END_DATETIME,
        "_order_by": "-End Time",
        "_limit": NUM_ROWS,
        "_only": col,
    }

    df = get_client.get_cycles(**query)

    assert df.shape == (NUM_ROWS, len(select_columns))

    select_columns = [
        "Machine",
        "Cycle Start Time",
        "End Time",
        "Production Day",
        "Cycle Time (Net)",
        "Cycle Time (Gross)",
    ]

    col = select_columns.copy()

    query = {
        "Machine": machine,
        "End Time__gte": START_DATETIME,
        "End Time__lte": END_DATETIME,
        "_order_by": "-End Time",
        "_limit": NUM_ROWS,
        "_only": col,
    }

    df = get_client.get_cycles(**query)

    assert df.shape == (NUM_ROWS, len(select_columns))
