import pandas as pd
from tests.conftest import TENANT
from smsdk.smsdk_entities.raw_data.raw_data import RawData

RAW_DATA_TABLE = "cycle_raw_data"
NUM_ROWS = 400
URL_V1 = "/v1/datatab/raw_data"


def test_get_utilities(get_session):
    raw_data = RawData(get_session, TENANT)

    # Run
    all_utilites = raw_data.get_utilities(get_session, URL_V1)

    expected_list = ["get_utilities", "get_raw_data"]

    assert len(all_utilites) == len(expected_list)
    assert all([a == b for a, b in zip(all_utilites, expected_list)])


def test_get_raw_data(get_client):
    timeselection = {
        "time_type": "absolute",
        "start_time": "2023-10-18T18:30:00.000Z",
        "end_time": "2023-10-19T18:29:59.999Z",
        "time_zone": "America/Los_Angeles",
    }
    select = []
    raw_data = get_client.get_raw_data(
        RAW_DATA_TABLE, fields=select, time_selection=timeselection
    )

    # check index
    assert raw_data.index.name == "_id"

    # check timestamp column
    assert "timestamp" in raw_data.columns.to_list()

    assert len(raw_data) == NUM_ROWS
    assert raw_data.shape == (400, 33)
