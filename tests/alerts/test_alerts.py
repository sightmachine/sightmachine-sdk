from typing import Dict, Any, List
import pandas as pd
from unittest.mock import patch, MagicMock
from smsdk.smsdk_entities.alerts.alerts import Alerts
from tests.conftest import TENANT
from tests.alerts.alerts_data import (
    ALERT_PAYLOAD,
    ALERT_UPDATES,
    UPDATED_ALERT,
    ALERTS_LIST,
    FILTERED_ALERTS,
)

# Define constants for test cases
ALERT_ID = 1
GROUP_NAME = "data_latency"


def test_update_alert_payload(get_session:Any)->None:
    alerts = Alerts(get_session, TENANT)
    assert alerts.update_alert_payload(ALERT_PAYLOAD, ALERT_UPDATES) == UPDATED_ALERT


def test_get_filtered_alerts_by_group(get_session:Any)->None:
    alerts = Alerts(get_session, TENANT)
    assert (
        alerts.get_filtered_alerts_by_group(ALERTS_LIST, GROUP_NAME) == FILTERED_ALERTS
    )


@patch.object(Alerts, "get_alert_config")
def test_get_alert_config(mock_get_alert_config:Dict[str,Any], get_session:Any)->None:
    mock_get_alert_config.return_value = ALERT_PAYLOAD

    alerts_instance = Alerts(get_session, TENANT)  # Create an instance
    assert alerts_instance.get_alert_config(1) == ALERT_PAYLOAD


@patch.object(Alerts, "update_alert")
def test_update_alert(mock_update_alert:bool, get_session:Any)-> None:
    mock_update_alert.return_value = True
    alerts_instance = Alerts(get_session, TENANT)  # Create an instance
    assert alerts_instance.update_alert(ALERT_ID, ALERT_UPDATES) == True


@patch.object(Alerts, "update_alert_group")
def test_update_alert_group(mock_update_alert_group:bool, get_session:Any)->None:
    mock_update_alert_group.return_value = True
    alerts_instance = Alerts(get_session, TENANT)
    assert alerts_instance.update_alert_group(GROUP_NAME, {"priority": "high"})


@patch.object(Alerts, "fetch_alerts_data")
def test_fetch_alerts_data(mock_fetch_alerts_data:List[Dict[str,Any]], get_session:Any)->None:
    mock_fetch_alerts_data.return_value = [ALERT_PAYLOAD]
    alerts_instance = Alerts(get_session, TENANT)
    assert alerts_instance.fetch_alerts_data() == [ALERT_PAYLOAD]


@patch.object(Alerts, "delete_alert")
def test_delete_alert(mock_delete_alert:bool, get_session:Any) ->None:
    mock_delete_alert.return_value = True
    alerts_instance = Alerts(get_session, TENANT)
    assert alerts_instance.delete_alert(ALERT_ID)


@patch.object(Alerts, "list_alerts")
def test_list_alerts(mock_list_alerts:List[str], get_session:Any) ->None:
    mock_list_alerts.return_value = ["alert1", "alert2"]
    alerts_instance = Alerts(get_session, TENANT)
    assert alerts_instance.list_alerts() == ["alert1", "alert2"]


@patch.object(Alerts, "get_alert_dataframe")
def test_get_alert_dataframe(mock_get_alert_dataframe:pd.DataFrame, get_session:Any) ->None:
    mock_df = MagicMock()
    mock_get_alert_dataframe.return_value = mock_df
    alerts_instance = Alerts(get_session, TENANT)
    assert alerts_instance.get_alert_dataframe() == mock_df
