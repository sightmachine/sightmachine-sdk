import pandas as pd
from datetime import datetime
from tests.conftest import TENANT
from smsdk.smsdk_entities.cycle.cycleV1 import Cycle
from tests.cycle.cycle_data import JSON_MACHINE_CYCLE_50


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
    machines = get_client.get_machine_names(source_type=MACHINE_TYPE)
    machine = machines[MACHINE_INDEX]
    columns = get_client.get_machine_schema(machine)["display"].to_list()

    query = {
        "Machine": machine,
        "End Time__gte": START_DATETIME,
        "End Time__lte": END_DATETIME,
        "_order_by": "-End Time",
        "_limit": NUM_ROWS,
        "_only": columns,
    }

    df = get_client.get_cycles(**query)

    assert df.shape == (NUM_ROWS, len(columns))


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

    assert df.shape != (NUM_ROWS, len(select_columns))

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
        # "Cycle Start Time",
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

    assert df.shape != (NUM_ROWS, len(select_columns))

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
