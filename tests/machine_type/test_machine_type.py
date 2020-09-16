import pandas as pd
from requests.sessions import Session
from tests.machine_type.machine_type_data import JSON_MACHINETYPE
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
