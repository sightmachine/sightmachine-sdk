from unittest.mock import MagicMock
from mock import patch
import pandas as pd
from requests.sessions import Session
from smsdk.client import Client
from tests.factory.factory_data import JSON_FACTORY
from smsdk.smsdk_entities.factory.factoryV1 import Factory


def test_get_factories(monkeypatch):
    # Setup
    def mockapi(self, session, endpoint):
        if endpoint == "/v1/obj/factory":
            return pd.DataFrame(JSON_FACTORY)
        return pd.DataFrame()

    monkeypatch.setattr(Factory, "get_factories", mockapi)

    dt = Factory(Session(), "demo")

    # Run
    df = dt.get_factories(Session(), "/v1/obj/factory")

    # Verify
    assert df.shape == (16, 13)

    cols = [
        "factory_id",
        "factory_location",
        "factory_location_clean",
        "factory_partner",
        "geo_location",
        "hash",
        "id",
        "metadata",
        "place_name",
        "schema_name",
        "shift_events",
        "shifts",
        "updatetime",
    ]
    assert cols == df.columns.sort_values().tolist()
