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

    dt = Machine(Session(), "demo-sdk-test")

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
        status_code = 200

        @staticmethod
        def json():
            return {"results": [{"machine": [{"name": "test", "type": "test_type"}]}]}

    mocked.return_value = MagicMock(get=MagicMock(return_value=ResponseGet()))

    dt = Client("demo-sdk-test")

    # Run
    type = dt.get_type_from_machine("test")

    # Verify
    assert type == "test_type"


@patch("smsdk.smsdk_entities.machine_type.machinetype.MachineType.get_fields")
@patch("smsdk.client.Client.get_type_from_machine")
def test_get_machine_schema(mocked_types, mocked_machines):
    mocked_machines.return_value = MACHINE_TYPE
    mocked_types.return_value = "test"
    dt = Client("demo-sdk-test")

    # Run
    fields = dt.get_machine_schema("test")
    assert fields.shape == (2, 3)
    # Verify
    assert fields.name.sort_values().tolist() == [
        "stat__test_float",
        "stat__test_string",
    ]


@patch("smsdk.smsdk_entities.machine_type.machinetype.MachineType.get_fields")
@patch("smsdk.client.Client.get_type_from_machine")
def test_get_machine_schema_hidden(mocked_types, mocked_machines):
    mocked_machines.return_value = MACHINE_TYPE
    mocked_types.return_value = "test"
    dt = Client("demo-sdk-test")

    # Run
    fields = dt.get_machine_schema("test", show_hidden=True)
    assert fields.shape == (3, 4)

    # Verify
    assert fields.name.sort_values().tolist() == [
        "stat__test_float",
        "stat__test_hidden",
        "stat__test_string",
    ]


@patch("smsdk.smsdk_entities.machine_type.machinetype.MachineType.get_fields")
@patch("smsdk.client.Client.get_type_from_machine")
def test_get_machine_schema_types(mocked_types, mocked_machines):
    mocked_machines.return_value = MACHINE_TYPE
    mocked_types.return_value = "test"
    dt = Client("demo-sdk-test")

    # Run
    fields = dt.get_machine_schema("test", types=["float"])
    assert fields.shape == (1, 3)

    # Verify
    assert fields.name.sort_values().tolist() == ["stat__test_float"]


@patch("smsdk.smsdk_entities.machine_type.machinetype.MachineType.get_fields")
@patch("smsdk.client.Client.get_type_from_machine")
def test_get_machine_schema_types_return_mtype(mocked_types, mocked_machines):
    mocked_machines.return_value = MACHINE_TYPE
    mocked_types.return_value = "test"
    dt = Client("demo-sdk-test")

    # Run
    fields = dt.get_machine_schema("test", return_mtype=True)
    assert fields[0] == "test"
    assert fields[1].shape == (2, 3)
    # Verify
    assert fields[1].name.sort_values().tolist() == [
        "stat__test_float",
        "stat__test_string",
    ]


"""
This test is against the demo-sdk-test environment and if the environment is changed then this test has to change as well.
"""


def test_get_machines_v1(get_client):
    machines = get_client.get_machines()
    assert machines.shape == (49, 10)


def test_get_machines_with_query_params(get_client):
    limit = 20
    query_params = {
        "_only": ["source", "source_clean", "source_type"],
        "source_type": "Lasercut",
        "_order_by": "source_clean",
        "_limit": limit,
    }
    machines = get_client.get_machines(**query_params)

    assert len(machines) == limit

    # Checking that we should only get these three columns that we have provided on query params.
    assert machines.columns.tolist() == ["source", "source_clean", "source_type"]
