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
    raw_data = get_client.get_raw_data(RAW_DATA_TABLE)
    assert len(raw_data)==NUM_ROWS