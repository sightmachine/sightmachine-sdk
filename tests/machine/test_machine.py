import pandas as pd
from requests.sessions import Session
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
