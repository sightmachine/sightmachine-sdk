import pandas as pd
from requests.sessions import Session
from tests.parts.part_data import JSON_PART

from smsdk.smsdk_entities.parts.partsV1 import Parts


def test_get_parts(monkeypatch):
    # Setup
    def mockapi(self, session, endpoint, **kwargs):
        if endpoint.startswith("/v1/datatab/part"):
            return pd.DataFrame(JSON_PART)
        return pd.DataFrame()

    monkeypatch.setattr(Parts, "get_parts", mockapi)

    dt = Parts(Session(), "demo")

    # Run
    df = dt.get_parts(Session(), "/v1/datatab/part")
    assert df.shape == (1, 29)

    cols = [
        "attachments",
        "batches",
        "capturetime",
        "capturetime_epoch",
        "codes",
        "endtime",
        "endtime_epoch",
        "id",
        "images",
        "localtz",
        "machine",
        "machine_sources",
        "machine_timestats",
        "metadata",
        "serial",
        "shift",
        "shiftid",
        "starttime",
        "starttime_epoch",
        "state",
        "stats",
        "status",
        "tombstone",
        "tombstone_epoch",
        "total",
        "type",
        "updatelocation",
        "updatetime",
        "version",
    ]

    assert cols == df.columns.sort_values().tolist()
