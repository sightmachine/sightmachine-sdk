from unittest.mock import MagicMock
from mock import patch
import pandas as pd
from requests.sessions import Session
from smsdk.client import Client
from tests.machine.machine_data import JSON_MACHINE, MACHINE_TYPE
from smsdk.smsdk_entities.machine.machine import Machine


# Define all the constants used in the test
LASERCUT_MACHINE_TYPE = "Lasercut"
MACHINE_INDEX = 0
MACHINE_NAMES_UI_BASED_EXPECT = [
    "Abidjan - Lasercut 1",
    "Abidjan - Lasercut 2",
    "Abidjan - Lasercut 3",
    "Bantam City - Lasercut 1",
    "Bantam City - Lasercut 2",
    "Bantam City - Lasercut 3",
    "Carmel - Lasercut 1",
    "Carmel - Lasercut 2",
    "Carmel - Lasercut 3",
    "Carmel - Lasercut 4",
    "Carmel - Lasercut 5",
    "Carmel - Lasercut 6",
    "Lima - Lasercut 1",
    "Lima - Lasercut 2",
    "Santa Catarina - Lasercut 1",
    "Santa Catarina - Lasercut 2",
    "Santa Catarina - Lasercut 3",
    "Singapore - Lasercut 1",
    "Singapore - Lasercut 2",
    "Singapore - Lasercut 3",
    "Singapore - Lasercut 4",
]
MACHINE_NAMES_INTERNAL_EXPECT = [
    "JB_AB_Lasercut_1",
    "JB_AB_Lasercut_2",
    "JB_AB_Lasercut_3",
    "JB_BT_Lasercut_1",
    "JB_BT_Lasercut_2",
    "JB_BT_Lasercut_3",
    "JB_CA_Lasercut_1",
    "JB_CA_Lasercut_2",
    "JB_CA_Lasercut_3",
    "JB_CA_Lasercut_4",
    "JB_CA_Lasercut_5",
    "JB_CA_Lasercut_6",
    "JB_LM_Lasercut_1",
    "JB_LM_Lasercut_2",
    "JB_SC_Lasercut_1",
    "JB_SC_Lasercut_2",
    "JB_SC_Lasercut_3",
    "JB_SG_Lasercut_1",
    "JB_SG_Lasercut_2",
    "JB_SG_Lasercut_3",
    "JB_SG_Lasercut_4",
]


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
def test_get_machine_schema_mock(mocked_types, mocked_machines):
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


def test_get_type_from_machine(get_client):
    machines = get_client.get_machine_names(LASERCUT_MACHINE_TYPE)
    machine = machines[MACHINE_INDEX]

    type = get_client.get_type_from_machine(machine)
    assert type == LASERCUT_MACHINE_TYPE


def test_get_machine_names(get_client):
    machines = get_client.get_machine_names(
        LASERCUT_MACHINE_TYPE,
        clean_strings_out=True,
    )
    assert sorted(machines) == MACHINE_NAMES_UI_BASED_EXPECT

    query = {
        "clean_strings_out": False,
        "source_type": LASERCUT_MACHINE_TYPE,
    }

    machines = get_client.get_machine_names(**query)
    assert sorted(machines) == MACHINE_NAMES_INTERNAL_EXPECT


def test_get_machine_schema(get_client):
    machine = MACHINE_NAMES_UI_BASED_EXPECT[MACHINE_INDEX]
    types = ["string", "int"]

    # Run
    df = get_client.get_machine_schema(machine)
    assert df.shape == (36, 15)

    # Run
    df = get_client.get_machine_schema(machine, types)
    assert df.shape == (16, 14)

    query = {"machine_source": machine, "types": types}

    # Run
    df = get_client.get_machine_schema(**query)
    assert df.shape == (16, 14)

    query = {"machine_source": machine, "types": types, "return_mtype": True}

    # Run
    df = get_client.get_machine_schema(**query)
    assert df[1].shape == (16, 14)
    assert df[0] == LASERCUT_MACHINE_TYPE
