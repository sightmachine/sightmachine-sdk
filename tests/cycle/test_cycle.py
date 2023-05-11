import pandas as pd
from requests.sessions import Session
from tests.cycle.cycle_data import JSON_MACHINE_CYCLE_50
from smsdk.smsdk_entities.cycle.cycle import Cycle


def test_get_cycles(monkeypatch):
    # Setup
    def mockapi(self, session, endpoint, **kwargs):
        if endpoint.startswith("/v1/datatab/cycle"):
            return pd.DataFrame(JSON_MACHINE_CYCLE_50)
        return pd.DataFrame()

    monkeypatch.setattr(Cycle, "get_cycles", mockapi)

    dt = Cycle(Session(), "demo")

    # Run
    df = dt.get_cycles(Session(), "/v1/datatab/cycle")

    assert df.shape == (50, 29)
