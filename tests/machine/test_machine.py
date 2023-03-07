from unittest.mock import MagicMock
from mock import patch
import pandas as pd
from requests.sessions import Session
from smsdk.client import Client
from tests.machine.machine_data import JSON_MACHINE
from smsdk.smsdk_entities.machine.machine import Machine


def test_get_machines(monkeypatch):
    # Setup
    def mockapi(self, session, endpoint):
        if endpoint == "/api/machine":
            return pd.DataFrame(JSON_MACHINE)
        return pd.DataFrame()

    monkeypatch.setattr(Machine, "get_machines", mockapi)

    dt = Machine(Session(), "demo")

    # Run
    df = dt.get_machines(Session(), "/api/machine")

    # Verify
    assert df.shape == (27, 7)

    cols = [
        "factory_location",
        "factory_partner",
        "id",
        "metadata",
        "source",
        "source_clean",
        "source_type",
    ]

    assert cols == df.columns.sort_values().tolist()


@patch("smsdk.ma_session.Session")
def test_get_type(mocked):
    class ResponseGet:
        ok = True
        text = "Success"
        status_code=200

        @staticmethod
        def json():
            return {'results':[{"machine":[{"name":"test", "type":'test_type'}]}]}

    mocked.return_value = MagicMock(
       get=MagicMock(return_value=ResponseGet())
    )

    dt = Client("demo")

    # Run
    type = dt.get_type_from_machine('test')

    # Verify
    assert type == 'test_type'
