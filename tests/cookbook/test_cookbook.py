import pandas as pd
from requests.sessions import Session
from smsdk.client import Client
from tests.cookbook.cookbook_data import AVALIBLE_KPI_JSON, KPI_DATA_VIZ_JSON
from smsdk.smsdk_entities.kpi.kpi import KPI
from mock import mock_open, MagicMock, patch

@patch("smsdk.ma_session.Session")
def test_get_cookbooks(mocked):
    class ResponseGet:
        ok = True
        text = "Success"
        status_code=200

        @staticmethod
        def json():
            return {"results": [{"kpi":AVALIBLE_KPI_JSON}]}
    mocked.return_value = MagicMock(
       get=MagicMock(return_value=ResponseGet())
    )

    dt = Client("demo")

    # Run
    kpis = dt.get_cookbooks()

    # Verify
    assert len(kpis) == 5

    assert kpis[0]["name"] == 'Scrap_Rate'