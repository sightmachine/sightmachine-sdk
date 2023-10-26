import pandas as pd
from datetime import datetime
from tests.conftest import TENANT
from smsdk.smsdk_entities.downtime.downtime import Downtime
from tests.downtime.downtime_data import JSON_MACHINE_DOWNTIME_100


# Define all the constants used in the test
MACHINE_TYPE = "Lasercut"
MACHINE_INDEX = 0
START_DATETIME = datetime(2023, 4, 1)
END_DATETIME = datetime(2023, 4, 2)
EXPECTED_ROWS = 18
EXPECTED_COL = 8
URL_V1 = "/v1/datatab/downtime"


def test_get_utilities(get_session):
    down_time = Downtime(get_session, TENANT)

    # Run
    all_utilites = down_time.get_utilities(get_session, URL_V1)

    expected_list = ["get_utilities", "get_downtime"]

    assert len(all_utilites) == len(expected_list)
    assert all([a == b for a, b in zip(all_utilites, expected_list)])


def test_get_downtime_monkeypatch(monkeypatch, get_session):
    # Setup
    def mockapi(self, session, endpoint, **kwargs):
        if endpoint.startswith(URL_V1):
            return pd.DataFrame(JSON_MACHINE_DOWNTIME_100)
        return pd.DataFrame()

    monkeypatch.setattr(Downtime, "get_downtime", mockapi)

    dt = Downtime(get_session, "demo-sdk-test")

    # Run
    df = dt.get_downtime(get_session, URL_V1)

    assert df.shape == (100, 22)


def test_get_downtime(get_client):
    machines = get_client.get_machine_names(source_type=MACHINE_TYPE)
    machine = machines[MACHINE_INDEX]

    query = {
        "Machine": machine,
        "End Time__gte": START_DATETIME,
        "End Time__lte": END_DATETIME,
        "_order_by": "-End Time",
    }

    df = get_client.get_downtimes(**query)

    assert df.shape == (EXPECTED_ROWS, EXPECTED_COL)
