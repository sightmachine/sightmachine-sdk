from unittest.mock import MagicMock
from mock import patch
import pandas as pd
from requests.sessions import Session
from smsdk.client import Client
from tests.machine.machine_data import JSON_MACHINE, MACHINE_TYPE
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


@patch("smsdk.client_v0.ClientV0.get_machines")
@patch("smsdk.client_v0.ClientV0.get_machine_types")
def test_get_machine_schema(mocked_types, mocked_machines):
    mocked_machines.return_value = {'source_type': ['test']}
    mocked_types.return_value = MACHINE_TYPE
    dt = Client("demo")

    # Run
    schema = dt.get_machine_schema('test')

    # Verify
    assert schema.name.sort_values().tolist() == ['stat__test_float', 'stat__test_string']


@patch("smsdk.client_v0.ClientV0.get_machines")
@patch("smsdk.client_v0.ClientV0.get_machine_types")
def test_get_machine_schema_hidden(mocked_types, mocked_machines):
    mocked_machines.return_value = {'source_type': ['test']}
    mocked_types.return_value = MACHINE_TYPE
    dt = Client("demo")

    # Run
    schema = dt.get_machine_schema('test', show_hidden=True)

    # Verify
    assert schema.name.sort_values().tolist() == ['stat__test_float', 'stat__test_hidden', 'stat__test_string']

@patch("smsdk.client_v0.ClientV0.get_machines")
@patch("smsdk.client_v0.ClientV0.get_machine_types")
def test_get_machine_schema_types(mocked_types, mocked_machines):
    mocked_machines.return_value = {'source_type': ['test']}
    mocked_types.return_value = MACHINE_TYPE
    dt = Client("demo")

    # Run
    schema = dt.get_machine_schema('test', types=["float"])

    # Verify
    assert schema.name.sort_values().tolist() == ['stat__test_float']

@patch("smsdk.client_v0.ClientV0.get_machines")
@patch("smsdk.client_v0.ClientV0.get_machine_types")
def test_get_machine_schema_types_return_mtype(mocked_types, mocked_machines):
    mocked_machines.return_value = {'source_type': ['test_type']}
    mocked_types.return_value = MACHINE_TYPE
    dt = Client("demo")

    # Run
    schema = dt.get_machine_schema('test', return_mtype=True)

    # Verify
    assert schema[0] == 'test_type'
    assert schema[1].name.sort_values().tolist() == ['stat__test_float', 'stat__test_string']

