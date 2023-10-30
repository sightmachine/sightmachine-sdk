import pandas as pd
from requests.sessions import Session
from smsdk.client import Client
from tests.kpi.kpi_data import AVALIBLE_KPI_JSON, KPI_DATA_VIZ_JSON
from smsdk.smsdk_entities.kpi.kpi import KPI
from mock import mock_open, MagicMock, patch


@patch("smsdk.ma_session.Session")
def test_get_kpi(mocked):
    class ResponseGet:
        ok = True
        text = "Success"
        status_code = 200

        @staticmethod
        def json():
            return {"results": [{"kpi": AVALIBLE_KPI_JSON}]}

    mocked.return_value = MagicMock(get=MagicMock(return_value=ResponseGet()))

    dt = Client("demo-sdk-test")

    # Run
    kpis = dt.get_kpis()

    # Verify
    assert len(kpis) == 5

    assert kpis[0]["name"] == "Scrap_Rate"


def test_get_kpi_for_asset(monkeypatch):
    # Setup
    def mockapi(self, session, endpoint):
        if endpoint == "/v1/selector/datavis/kpi/y_axis":
            return pd.DataFrame(AVALIBLE_KPI_JSON)
        return pd.DataFrame()

    monkeypatch.setattr(KPI, "get_kpis_for_asset", mockapi)

    dt = KPI(Session(), "demo-sdk-test")

    # Run
    df = dt.get_kpis_for_asset(Session(), "/v1/selector/datavis/kpi/y_axis")

    # Verify
    assert df.shape == (5, 7)

    names = ["Scrap_Rate", "availability", "oee", "performance", "quality"]

    assert names == df.name.sort_values().tolist()


@patch("smsdk.ma_session.Session")
def test_get_kpi_data_viz(mocked):
    class ResponsePost:
        ok = True
        text = "Success"
        status_code = 200

        @staticmethod
        def json():
            return {"response": {"task_id": "test"}}

    class ResponseGet:
        ok = True
        text = "Success"
        status_code = 200

        @staticmethod
        def json():
            return {
                "response": {"state": "SUCCESS", "meta": {"results": KPI_DATA_VIZ_JSON}}
            }

    mocked.return_value = MagicMock(
        post=MagicMock(return_value=ResponsePost()),
        get=MagicMock(return_value=ResponseGet()),
    )

    dt = Client("demo-sdk-test")
    data = dt.get_kpi_data_viz()
    assert len(data) == 3
    assert data[0]["d_vals"]["quality"]["avg"] == 95.18072289156626


def test_kpi_for_asset_display_name(get_client):
    kpis = ["performance", "oee", "quality", "availability"]
    # Query against machine type system name and machine source system name
    query = {
        "asset_selection": {
            "machine_type": ["PickAndPlace"],
            "machine_source": ["JB_NG_PickAndPlace_1_Stage6"],
        }
    }
    df1 = get_client.get_kpis_for_asset(**query)
    assert len(df1) > 0
    assert df1[0]["name"] in kpis

    # Query against machine type display name and machine source display name
    query = {
        "asset_selection": {
            "machine_type": ["Pick & Place"],
            "machine_source": ["Nagoya - Pick and Place 6"],
        }
    }
    df2 = get_client.get_kpis_for_asset(**query)
    assert len(df2) > 0
    assert df2[0]["name"] in kpis

    assert df1 == df2


def test_get_kpi_data_viz(get_client):
    data_viz_query = {
        "asset_selection": {
            "machine_source": ["JB_NG_PickAndPlace_1_Stage6"],
            "machine_type": ["PickAndPlace"],
        },
        "d_vars": [{"name": "quality", "aggregate": ["avg"]}],
        "i_vars": [
            {
                "name": "endtime",
                "time_resolution": "day",
                "query_tz": "America/Los_Angeles",
                "output_tz": "America/Los_Angeles",
                "bin_strategy": "user_defined2",
                "bin_count": 50,
            }
        ],
        "time_selection": {
            "time_type": "relative",
            "relative_start": 7,
            "relative_unit": "year",
            "ctime_tz": "America/Los_Angeles",
        },
        "where": [],
        "db_mode": "sql",
    }

    df1 = get_client.get_kpi_data_viz(**data_viz_query)

    data_viz_query = {
        "asset_selection": {
            "machine_source": ["Nagoya - Pick and Place 6"],
            "machine_type": ["Pick & Place"],
        },
        "d_vars": [{"name": "quality", "aggregate": ["avg"]}],
        "i_vars": [
            {
                "name": "endtime",
                "time_resolution": "day",
                "query_tz": "America/Los_Angeles",
                "output_tz": "America/Los_Angeles",
                "bin_strategy": "user_defined2",
                "bin_count": 50,
            }
        ],
        "time_selection": {
            "time_type": "relative",
            "relative_start": 7,
            "relative_unit": "year",
            "ctime_tz": "America/Los_Angeles",
        },
        "where": [],
        "db_mode": "sql",
    }

    df2 = get_client.get_kpi_data_viz(**data_viz_query)

    assert len(df1) == len(df2)
