import pandas as pd
from smsdk.client import Client
from tests.conftest import TENANT
from smsdk.smsdk_entities.line.line import Line
from mock import mock_open, MagicMock, patch
from tests.lines.line_data import AVALIBLE_LINE_JSON, LINE_DATA_JSON


# # Define all the constants used in the test
START_DATETIME = "2023-04-01T08:00:00.000Z"
END_DATETIME = "2023-04-02T23:00:00.000Z"
TIME_ZONE = "America/Los_Angeles"
MAX_ROWS = 50
LINE_INDEX = 0
EXP_NUM_LINES = 1
NAME_ATRIB = "name"
LINE_NAME = "JB_NG_PickAndPlace_1"
MACHINE4 = "JB_NG_PickAndPlace_1_Stage4"
FIELD_NAME1 = "stats__BLOCKED__val"
FIELD_NAME2 = "stats__PneumaticPressure__val"
MIN_PRESSURE = 75.25
EXP_NUM_ROWS = 14
URL_V1 = "/v1/datatab/line"


def test_get_utilities(get_session):
    line = Line(get_session, TENANT)

    # Run
    all_utilites = line.get_utilities(get_session, URL_V1)

    expected_list = ["get_utilities", "get_lines", "get_line_data"]

    assert len(all_utilites) == len(expected_list)
    assert all([a == b for a, b in zip(all_utilites, expected_list)])


def test_get_lines(get_client):
    # Call the get_lines API
    lines = get_client.get_lines()

    # Verify
    assert len(lines) == EXP_NUM_LINES
    assert lines[LINE_INDEX][NAME_ATRIB] == LINE_NAME


def test_get_line_data(get_client):
    assets = [MACHINE4]
    fields = [
        {"asset": MACHINE4, "name": FIELD_NAME1},
        {"asset": MACHINE4, "name": FIELD_NAME2},
    ]

    time_selection = {
        "time_type": "absolute",
        "start_time": START_DATETIME,
        "end_time": END_DATETIME,
        "time_zone": TIME_ZONE,
    }

    filters = [
        {
            "asset": MACHINE4,
            "name": FIELD_NAME2,
            "op": "gte",
            "value": MIN_PRESSURE,
        }
    ]

    df1 = get_client.get_line_data(
        assets, fields, time_selection, filters=filters, limit=MAX_ROWS
    )

    assert len(df1) == EXP_NUM_ROWS

    # Check each element in the df for the pneumatic pressure
    for i, expected_value in enumerate(df1):
        assert df1[i][f"{MACHINE4}:{FIELD_NAME2}"] >= MIN_PRESSURE

    query = {
        "assets": assets,
        "fields": fields,
        "time_selection": time_selection,
        "filters": filters,
        "limit": MAX_ROWS,
    }

    df2 = get_client.get_line_data(**query)

    assert df1 == df2
