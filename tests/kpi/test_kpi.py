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

    dt = Client("demo")

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

    dt = KPI(Session(), "demo")

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

    dt = Client("demo")
    data = dt.get_kpi_data_viz()
    assert len(data) == 3
    assert data[0]["d_vals"]["quality"]["avg"] == 95.18072289156626
