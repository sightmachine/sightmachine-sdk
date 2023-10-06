from mock import patch
import pandas as pd
from requests.sessions import Session
from smsdk.client import Client
from tests.machine_type.machine_type_data import JSON_MACHINETYPE, MACHINE_TYPE_FIELDS
from smsdk.smsdk_entities.machine_type.machinetype import MachineType


def test_get_machine_types(monkeypatch):
    # Setup
    def mockapi(self, session, endpoint):
        if endpoint == "/api/machinetype":
            return pd.DataFrame(JSON_MACHINETYPE)
        return pd.DataFrame()

    monkeypatch.setattr(MachineType, "get_machine_types", mockapi)

    dt = MachineType(Session(), "demo")

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
def test_get_fields_of_machine_type(mocked_machines):
    mocked_machines.return_value = MACHINE_TYPE_FIELDS
    dt = Client("demo")

    # Run
    fields = dt.get_fields_of_machine_type("test")
    assert len(fields) == 2
    names = [field["name"] for field in fields]
    # Verify
    assert names == ["stat__test_float", "stat__test_string"]


@patch("smsdk.smsdk_entities.machine_type.machinetype.MachineType.get_fields")
def test_get_fields_of_machine_type_hidden(mocked_machines):
    mocked_machines.return_value = MACHINE_TYPE_FIELDS
    dt = Client("demo")

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
    dt = Client("demo")

    # Run
    fields = dt.get_fields_of_machine_type("test", types=["float"])
    assert len(fields) == 1
    names = [field["name"] for field in fields]

    # Verify
    assert names == ["stat__test_float"]


def test_get_machines_types_v1(get_client):
    machine_types = get_client.get_machine_types()
    assert machine_types.shape == (114, 25)
