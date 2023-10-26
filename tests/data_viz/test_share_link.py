from smsdk.client import Client
from mock import patch


@patch("smsdk.ma_session.Session.post")
@patch("smsdk.client.Client.get_type_from_machine")
def test_cycle_share_link(mock_type, mocked):
    class ResponsePost:
        ok = True
        text = "Success"
        status_code = 200

        @staticmethod
        def json():
            return {"state_hash": "test"}

    mocked.return_value = ResponsePost()
    mock_type.return_value = "test_machine"

    dt = Client("demo-sdk-test")

    # Run
    sharelink = dt.create_share_link(["test"], "line", {"id": "cans"})

    # Verify
    assert (
        sharelink == "https://demo-sdk-test.sightmachine.io/#/analysis/datavis/s/test"
    )
    assert mocked.call_args[1]["json"]["state"]["asset"] == {
        "machine_source": ["test"],
        "machine_type": ["test_machine"],
    }


@patch("smsdk.ma_session.Session.post")
@patch("smsdk.client.Client.get_type_from_machine")
def test_kpi_share_link(mock_type, mocked):
    class ResponsePost:
        ok = True
        text = "Success"
        status_code = 200

        @staticmethod
        def json():
            return {"state_hash": "test"}

    mocked.return_value = ResponsePost()
    mock_type.return_value = "test_machine"

    dt = Client("demo-sdk-test")

    # Run
    sharelink = dt.create_share_link(["test"], "line", {"id": "cans"}, model="kpi")

    # Verify
    assert (
        sharelink == "https://demo-sdk-test.sightmachine.io/#/analysis/datavis/s/test"
    )
    assert mocked.call_args[1]["json"]["state"]["asset"] == {
        "machine_source": ["test"],
        "machine_type": ["test_machine"],
    }
    assert mocked.call_args[1]["json"]["state"]["yAxisMulti"] == [{"id": "cans"}]


@patch("smsdk.ma_session.Session.post")
@patch("smsdk.client.Client.get_type_from_machine")
def test_line_share_link(mock_type, mocked):
    class ResponsePost:
        ok = True
        text = "Success"
        status_code = 200

        @staticmethod
        def json():
            return {"state_hash": "test"}

    mocked.return_value = ResponsePost()
    mock_type.return_value = "test_machine"

    dt = Client("demo-sdk-test")

    # Run
    sharelink = dt.create_share_link(
        ["test"], "line", {"field": "cans", "machineName": "test"}, model="line"
    )

    # Verify
    assert (
        sharelink == "https://demo-sdk-test.sightmachine.io/#/analysis/datavis/s/test"
    )
    assert mocked.call_args[1]["json"]["state"]["lineProcess"] == {
        "selectedMachines": [{"machineName": "test"}]
    }
    assert mocked.call_args[1]["json"]["state"]["lineYAxisMulti"] == [
        {
            "field": {"name": "cans", "machine_type": {"name": "test_machine"}},
            "machineName": "test",
        }
    ]


@patch("smsdk.ma_session.Session.post")
@patch("smsdk.client.Client.get_type_from_machine")
def test_line_offset_share_link(mock_type, mocked):
    class ResponsePost:
        ok = True
        text = "Success"
        status_code = 200

        @staticmethod
        def json():
            return {"state_hash": "test"}

    mocked.return_value = ResponsePost()
    mock_type.return_value = "test_machine"

    dt = Client("demo-sdk-test")

    # Run
    sharelink = dt.create_share_link(
        {
            "assets": ["test"],
            "assetOffsets": {"test": {"period": 1, "interval": "minutes"}},
        },
        "line",
        {"field": "cans", "machineName": "test"},
        model="line",
    )

    # Verify
    assert (
        sharelink == "https://demo-sdk-test.sightmachine.io/#/analysis/datavis/s/test"
    )
    assert mocked.call_args[1]["json"]["state"]["lineProcess"] == {
        "assetOffsets": {"test": {"interval": "minutes", "period": 1}},
        "selectedMachines": [{"machineName": "test"}],
    }
    assert mocked.call_args[1]["json"]["state"]["lineYAxisMulti"] == [
        {
            "field": {"name": "cans", "machine_type": {"name": "test_machine"}},
            "machineName": "test",
        }
    ]
