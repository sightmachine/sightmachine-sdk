import pandas as pd
from requests.sessions import Session
from smsdk.client import Client
from tests.cookbook.cookbook_data import AVALIBLE_COOKBOOK_JSON, RUNS, CURRENT_VALUE
from smsdk.smsdk_entities.kpi.kpi import KPI
from mock import mock_open, MagicMock, patch


# Define all the constants used in the test
VALUE_EXPC = [{"asset": "test", "name": "test_field", "values": {"latest": 42.42}}]


@patch("smsdk.ma_session.Session")
def test_get_cookbooks(mocked):
    class ResponseGet:
        ok = True
        text = "Success"
        status_code = 200

        @staticmethod
        def json():
            return {"objects": AVALIBLE_COOKBOOK_JSON}

    mocked.return_value = MagicMock(get=MagicMock(return_value=ResponseGet()))

    dt = Client("demo-sdk-test")

    # Run
    cookbooks = dt.get_cookbooks()

    # Verify
    assert len(cookbooks) == 1

    assert cookbooks[0]["name"] == "Test cookbook"


@patch("smsdk.ma_session.Session")
def test_get_top_results(mocked):
    class ResponseGet:
        ok = True
        text = "Success"
        status_code = 200

        @staticmethod
        def json():
            return RUNS

    mocked.return_value = MagicMock(get=MagicMock(return_value=ResponseGet()))

    dt = Client("demo-sdk-test")

    # Run
    runs = dt.get_cookbook_top_results("recipe_group_id", 1)

    # Verify
    assert len(runs["runs"]) == 1

    query = {
        "recipe_group_id": "recipe_group_id",
        "limit": 1,
    }

    runs = dt.get_cookbook_top_results(**query)

    # Verify
    assert len(runs["runs"]) == 1


@patch("smsdk.ma_session.Session")
def test_get_current_value(mocked):
    class ResponseGet:
        ok = True
        text = "Success"
        status_code = 200

        @staticmethod
        def json():
            return {"results": CURRENT_VALUE}

    mocked.return_value = MagicMock(post=MagicMock(return_value=ResponseGet()))

    dt = Client("demo-sdk-test")

    # Run
    value = dt.get_cookbook_current_value([{"asset": "test", "name": "test_field"}])

    # Verify
    assert value[0]["values"]["latest"] == 42.42

    query = {
        "variables": [{"asset": "test", "name": "test_field"}],
        "minutes": 1440,
    }

    # Run
    value = dt.get_cookbook_current_value(**query)

    # Verify
    assert VALUE_EXPC == value
