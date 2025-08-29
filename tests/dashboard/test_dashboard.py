from smsdk.smsdk_entities.dashboard.dashboard import DashboardData
from smsdk.client import Client
from mock import patch, MagicMock
import unittest


@patch("smsdk.ma_session.Session")
def test_get_dashboard(mocked):
    class ResponseGet:
        ok = True
        text = "Success"
        status_code = 200

        @staticmethod
        def json():
            return {"panels": [{"id": 1, "name": "Panel_1"}]}

    mocked.return_value = MagicMock(get=MagicMock(return_value=ResponseGet()))

    dt = Client("demo-sdk-test")

    # Run
    panels = dt.get_dashboard("dashboard_id_1")

    # Verify
    assert isinstance(panels, list)
    assert panels[0]["id"] == 1
    assert panels[0]["name"] == "Panel_1"


@patch("smsdk.ma_session.Session")
def test_dashboard_for_incorrect_id(mocked):
    class ResponseGet:
        ok = False
        text = "Not Found"
        status_code = 404

        @staticmethod
        def json():
            return {"error": "Dashboard not found"}

    mocked.return_value = MagicMock(get=MagicMock(return_value=ResponseGet()))

    dt = Client("demo-sdk-test")

    # Expecting a ValueError or custom NotFound exception for incorrect dashboard_id
    with unittest.TestCase().assertRaises(ValueError):
        dt.get_dashboard("invalid_dashboard_id")
