from smsdk.smsdk_entities.workspace.workspace import Workspace
from smsdk.client import Client
from mock import patch, MagicMock
import unittest


@patch("smsdk.ma_session.Session")
def test_get_workspace(mocked):
    class ResponseGet:
        ok = True
        text = "Success"
        status_code = 200

        @staticmethod
        def json():
            return {"workspaces": [{"id": 1, "name": "Workspace_1"}]}

    mocked.return_value = MagicMock(get=MagicMock(return_value=ResponseGet()))

    dt = Client("demo-sdk-test")

    # Run
    workspaces = dt.get_workspace("workspace_id_1")

    # Verify
    assert isinstance(workspaces, list)
    assert workspaces[0]["id"] == 1
    assert workspaces[0]["name"] == "Workspace_1"


@patch("smsdk.ma_session.Session")
def test_workspace_for_incorrect_schema(mocked):
    class ResponseGet:
        ok = False
        text = "Not Found"
        status_code = 404

        @staticmethod
        def json():
            return {"error": "Workspace not found"}

    mocked.return_value = MagicMock(get=MagicMock(return_value=ResponseGet()))

    dt = Client("demo-sdk-test")

    # Expecting a ValueError or custom NotFound exception for incorrect workspace_id
    with unittest.TestCase.assertRaises(dt, ValueError):
        dt.get_workspace("invalid_workspace_id")
