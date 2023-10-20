import pandas as pd
from datetime import datetime
from tests.conftest import TENANT
from smsdk.smsdk_entities.factory.factory import Factory


# Define all the constants used in the test
NUM_ROWS = 10
NUM_COL = 3
URL = "/api/factory"


def test_get_utilities(get_session):
    factory = Factory(get_session, TENANT)

    # Run
    all_utilites = factory.get_utilities(get_session, URL)

    expected_list = ["get_utilities", "get_factories"]

    assert len(all_utilites) == len(expected_list)
    assert all([a == b for a, b in zip(all_utilites, expected_list)])


def test_get_factories(get_client):
    query = {
        "_order_by": "-End Time",
        "_only": ["factory_id", "factory_location", "place_name"],
        "_limit": NUM_ROWS,
    }

    df = get_client.get_factories(**query)

    assert df.shape == (NUM_ROWS, NUM_COL)
