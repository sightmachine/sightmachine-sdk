from mock import patch
import pandas as pd
from requests.sessions import Session
from smsdk.client import Client
from tests.machine_type.machine_type_data import JSON_MACHINETYPE, MACHINE_TYPE_FIELDS
from smsdk.smsdk_entities.machine_type.machinetype import MachineType


MACHINE_TYPE_NAMES_UI_BASED_EXPECT = ["Lasercut", "Pick & Place", "Diecast", "Fusion"]
MACHINE_TYPE_NAMES_INTERNAL_EXPECT = ["Lasercut", "PickAndPlace", "Diecast", "Fusion"]


def test_get_machine_types_mock(monkeypatch):
    # Setup
    def mockapi(self, session, endpoint):
        if endpoint == "/api/machinetype":
            return pd.DataFrame(JSON_MACHINETYPE)
        return pd.DataFrame()

    monkeypatch.setattr(MachineType, "get_machine_types", mockapi)

    dt = MachineType(Session(), "demo-sdk-test")

    # Run
    df = dt.get_machine_types(Session(), "/api/machinetype")

    # Verify
    assert df.shape == (2, 22)

    cols = [
        "analytics",
        "capturetime",
        "capturetime_epoch",
        "cmdr_meta",
        "etlpluginmap",
        "etlsettings",
        "id",
        "localtz",
        "meta_assign",
        "metadata",
        "part_type",
        "recipes",
        "scaffold",
        "source_type",
        "source_type_clean",
        "stats",
        "tag",
        "tombstone",
        "tombstone_epoch",
        "updatelocation",
        "updatetime",
        "version",
    ]

    assert cols == df.columns.sort_values().tolist()


@patch("smsdk.smsdk_entities.machine_type.machinetype.MachineType.get_fields")
def test_get_fields_of_machine_type_mock(mocked_machines):
    mocked_machines.return_value = MACHINE_TYPE_FIELDS
    dt = Client("demo-sdk-test")

    # Run
    fields = dt.get_fields_of_machine_type("test")
    assert len(fields) == 2
    names = [field["name"] for field in fields]
    # Verify
    assert names == ["stat__test_float", "stat__test_string"]


@patch("smsdk.smsdk_entities.machine_type.machinetype.MachineType.get_fields")
def test_get_fields_of_machine_type_hidden(mocked_machines):
    mocked_machines.return_value = MACHINE_TYPE_FIELDS
    dt = Client("demo-sdk-test")

    # Run
    fields = dt.get_fields_of_machine_type("test", show_hidden=True)
    assert len(fields) == 3
    names = [field["name"] for field in fields]
    names.sort()

    # Verify
    assert names == ["stat__test_float", "stat__test_hidden", "stat__test_string"]


@patch("smsdk.smsdk_entities.machine_type.machinetype.MachineType.get_fields")
def test_get_fields_of_machine_type_types(mocked_machines):
    mocked_machines.return_value = MACHINE_TYPE_FIELDS
    dt = Client("demo-sdk-test")

    # Run
    fields = dt.get_fields_of_machine_type("test", types=["float"])
    assert len(fields) == 1
    names = [field["name"] for field in fields]

    # Verify
    assert names == ["stat__test_float"]


"""
This test is against the demo-sdk-test environment and if the environment is changed then this test has to change as well.
"""


def test_get_machines_types(get_client):
    machine_types = get_client.get_machine_types()
    unique_machine_types = machine_types["source_type"].dropna().unique()
    assert unique_machine_types.tolist() == MACHINE_TYPE_NAMES_INTERNAL_EXPECT

    query = {
        "source_type": "Lasercut",
    }

    machine_types = get_client.get_machine_types(**query)
    assert machine_types.shape == (29, 25)


def test_get_machines_types_v1(get_client):
    machine_types = get_client.get_machine_types()
    assert machine_types.shape == (114, 25)


def test_get_machines_type_names_v1(get_client):
    machine_types_ui_based = get_client.get_machine_type_names()
    assert machine_types_ui_based == MACHINE_TYPE_NAMES_UI_BASED_EXPECT

    query = {
        "clean_strings_out": False,
    }

    machine_types_internal = get_client.get_machine_type_names(**query)
    assert machine_types_internal == MACHINE_TYPE_NAMES_INTERNAL_EXPECT


def test_get_fields_of_machine_type(get_client):
    machine_type = "Lasercut"
    types = ["string", "int"]

    # Run
    fields = get_client.get_fields_of_machine_type(machine_type)
    assert len(fields) == 36

    # Run
    fields = get_client.get_fields_of_machine_type(machine_type, types)
    assert len(fields) == 16

    query = {
        "machine_type": machine_type,
        "types": types,
        "show_hidden": True,
    }

    # Run
    fields = get_client.get_fields_of_machine_type(**query)
    assert len(fields) == 16
