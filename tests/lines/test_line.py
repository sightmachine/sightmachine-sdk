import pandas as pd
from requests.sessions import Session
from smsdk.client import Client
from smsdk.smsdk_entities.line.line import Line
from mock import mock_open, MagicMock, patch

from tests.lines.line_data import AVALIBLE_LINE_JSON, LINE_DATA_JSON


@patch("smsdk.ma_session.Session")
def test_get_lines(mocked):
    class ResponseGet:
        ok = True
        text = "Success"
        status_code = 200

        @staticmethod
        def json():
            return {"results": [{"line": AVALIBLE_LINE_JSON}]}

    mocked.return_value = MagicMock(get=MagicMock(return_value=ResponseGet()))

    dt = Client("demo")

    # Run
    lines = dt.get_lines()

    # Verify
    assert len(lines) == 6

    assert lines[0]["name"] == "F2_CANNING_L1"


@patch("smsdk.ma_session.Session")
def test_get_line_data(mocked):
    class ResponsePost:
        ok = True
        text = "Success"
        status_code = 200

        @staticmethod
        def json():
            return {"results": LINE_DATA_JSON}

    mocked.return_value = MagicMock(post=MagicMock(return_value=ResponsePost()))

    dt = Client("demo")
    data = dt.get_line_data(["test"])
    assert len(data) == 3
    assert data[0]["F2_010_BodyMaker_1:stats__0_BM 008: Cans Out__val"] == 35440.0
