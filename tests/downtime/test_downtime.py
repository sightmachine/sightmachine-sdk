import pandas as pd
from requests.sessions import Session
from tests.downtime.downtime_data import JSON_MACHINE_DOWNTIME_100

from smsdk.smsdk_entities.downtime.downtime import Downtime


def test_get_downtime(monkeypatch):
    # Setup
    def mockapi(self, session, endpoint, **kwargs):
        if endpoint.startswith("/api/downtime"):
            return pd.DataFrame(JSON_MACHINE_DOWNTIME_100)
        return pd.DataFrame()

    monkeypatch.setattr(Downtime, "get_downtime", mockapi)

    dt = Downtime(Session(), "demo")

    # Run
    df = dt.get_downtime(Session(), "/api/downtime")

    assert df.shape == (100, 22)
