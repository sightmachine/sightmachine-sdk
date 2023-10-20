import pandas as pd
from datetime import datetime
from tests.conftest import TENANT
from tests.parts.part_data import JSON_PART
from smsdk.smsdk_entities.parts.partsV1 import Parts


# Define all the constants used in the test
MACHINE_TYPE = "Lasercut"
PART_TYPE_INDEX = 1
START_DATETIME = datetime(2023, 4, 1)
END_DATETIME = datetime(2023, 4, 2)
NUM_ROWS = 10
NUM_COLUMNS_FOR_QUERY = 31
URL_V1 = "/v1/datatab/part"


def test_get_utilities(get_session):
    part = Parts(get_session, TENANT)

    # Run
    all_utilites = part.get_utilities(get_session, URL_V1)

    expected_list = ["get_utilities", "get_parts"]

    assert len(all_utilites) == len(expected_list)
    assert all([a == b for a, b in zip(all_utilites, expected_list)])


def test_get_parts_monkeypatch(monkeypatch, get_session):
    # Setup
    def mockapi(self, session, endpoint, **kwargs):
        if endpoint.startswith(URL_V1):
            return pd.DataFrame(JSON_PART)
        return pd.DataFrame()

    monkeypatch.setattr(Parts, "get_parts", mockapi)

    dt = Parts(get_session, TENANT)

    # Run
    df = dt.get_parts(get_session, URL_V1)
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


def test_get_parts(get_client):
    part_types = get_client.get_part_type_names()
    part_type = part_types[PART_TYPE_INDEX]

    columns = get_client.get_part_schema(part_type)["display"].to_list()

    query = {
        "Part": part_type,
        "End Time__gte": START_DATETIME,
        "End Time__lte": END_DATETIME,
        "DefectReason__exists": True,
        "_limit": NUM_ROWS,
        "_only": columns[: NUM_COLUMNS_FOR_QUERY - 1],
    }

    df = get_client.get_parts(**query)

    assert df.shape == (NUM_ROWS, NUM_COLUMNS_FOR_QUERY)
