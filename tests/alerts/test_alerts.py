from typing import Any
from unittest.mock import MagicMock

import numpy as np
import pandas as pd

from smsdk.smsdk_entities.alerts.alerts import Alerts
from tests.conftest import TENANT
from tests.alerts.alerts_data import (
    ALERT_PAYLOAD,
    ALERT_UPDATES,
    UPDATED_ALERT,
    ALERTS_LIST,
    FILTERED_ALERTS,
)


def _make_alerts(get_session: Any) -> Alerts:
    return Alerts(get_session, TENANT or "genmills-ms-rbg")


def test_update_alert_payload(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    assert alerts.update_alert_payload(ALERT_PAYLOAD, ALERT_UPDATES) == UPDATED_ALERT


def test_get_updated_alert_nested_merge(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    existing = {"a": {"b": 1, "c": [1, 2]}, "remove_me": 0, "display_name": "x"}
    updates = {"a": {"b": 2, "c": [3, 4]}, "display_name": "y", "incident_total": 5}
    merged = alerts.get_updated_alert(existing, updates)
    assert merged["a"]["b"] == 2
    assert merged["a"]["c"] == [3, 4]
    assert merged["display_name"] == "y"
    assert "incident_total" not in merged


def test_get_filtered_alerts_by_group(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    assert alerts.get_filtered_alerts_by_group(ALERTS_LIST, "data_latency") == FILTERED_ALERTS
    assert alerts.get_filtered_alerts_by_group(ALERTS_LIST, "unknown") == []


def test_get_alert_config_success(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    alerts.session = MagicMock()
    alerts.session.get.return_value.status_code = 200
    alerts.session.get.return_value.json.return_value = ALERT_PAYLOAD
    assert alerts.get_alert_config("1") == ALERT_PAYLOAD


def test_get_alert_config_failure(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    alerts.session = MagicMock()
    alerts.session.get.return_value.status_code = 500
    alerts.session.get.return_value.text = "boom"
    assert alerts.get_alert_config("1") is None


def test_update_alert_success(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    alerts.session = MagicMock()
    # Mock dependencies
    alerts.get_alert_config = MagicMock(return_value=ALERT_PAYLOAD)  # type: ignore
    alerts.update_alert_payload = MagicMock(return_value=UPDATED_ALERT)  # type: ignore
    alerts.session.put.return_value.status_code = 200
    alerts.update_alert("1", ALERT_UPDATES)
    alerts.session.put.assert_called_once()
    args, kwargs = alerts.session.put.call_args
    assert kwargs.get("json") == UPDATED_ALERT


def test_update_alert_error_response(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    alerts.session = MagicMock()
    alerts.get_alert_config = MagicMock(return_value=ALERT_PAYLOAD)  # type: ignore
    alerts.update_alert_payload = MagicMock(return_value=UPDATED_ALERT)  # type: ignore
    alerts.session.put.return_value.status_code = 500
    alerts.session.put.return_value.text = "err"
    alerts.update_alert("1", ALERT_UPDATES)
    alerts.session.put.assert_called_once()


def test_update_alert_no_params_does_not_call_put(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    alerts.session = MagicMock()
    alerts.update_alert("1", {})
    alerts.session.put.assert_not_called()


def test_update_alert_group_happy_path(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    alerts.session = MagicMock()
    alerts.get_alert_config = MagicMock(return_value=ALERT_PAYLOAD)  # type: ignore
    alerts.session.put.return_value.status_code = 200
    df = pd.DataFrame([
        {"id": ALERT_PAYLOAD["id"], "display_name": "New Name"}
    ])
    alerts.update_alert_group(df)
    alerts.session.put.assert_called_once()


def test_fetch_alerts_data_success_and_failure(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    alerts.session = MagicMock()
    alerts.session.get.return_value.status_code = 200
    alerts.session.get.return_value.json.return_value = {"objects": [ALERT_PAYLOAD]}
    assert alerts.fetch_alerts_data() == [ALERT_PAYLOAD]
    alerts.session.get.return_value.status_code = 400
    alerts.session.get.return_value.text = "nope"
    assert alerts.fetch_alerts_data() == []


def test_list_alerts_filters_and_transforms(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    # Stub upstream data provider
    alerts.fetch_alerts_data = MagicMock(return_value=ALERTS_LIST)  # type: ignore
    # Filter by data_latency
    df = alerts.list_alerts("data_latency")
    assert df is not None
    assert set([*df.columns]) == {"display_name", "analytic", "Creator", "status", "incident_count"}
    assert (df["analytic"] == "DataLatencyAlertingETL3").all()
    # No filter returns rows
    df_all = alerts.list_alerts("")
    assert df_all is not None
    assert len(df_all) >= len(df)


def test_get_alert_dataframe_empty_when_no_ids(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    alerts.fetch_alerts_data = MagicMock(return_value=[])  # type: ignore
    df = alerts.get_alert_dataframe("")
    assert isinstance(df, pd.DataFrame)
    assert df.empty


def test_get_alert_dataframe_happy_path(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    sample_ids = ["id1", "id2"]
    base_list = [{"id": i, "analytic": {"plugin_id": "DataLatencyAlertingETL3"}} for i in sample_ids]
    alerts.fetch_alerts_data = MagicMock(return_value=base_list)  # type: ignore
    alerts.get_alert_config = MagicMock(return_value=ALERT_PAYLOAD)  # type: ignore
    df = alerts.get_alert_dataframe("data_latency")
    assert not df.empty
    # Check a few representative columns exist
    for col in [
        "analytic___plugin_id",
        "notification___backend___email___subject",
        "analytic___plugin_parameters___alert_config___max_latency",
    ]:
        assert col in df.columns


def test_delete_alert_invalid_id_does_not_call_delete(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    alerts.session = MagicMock()
    alerts.fetch_alerts_data = MagicMock(return_value=[{"id": "a"}])  # type: ignore
    alerts.delete_alert("not-found", False, "")
    alerts.session.delete.assert_not_called()


def test_delete_alert_single_success(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    alerts.session = MagicMock()
    alerts.fetch_alerts_data = MagicMock(return_value=[{"id": "a"}])  # type: ignore
    alerts.session.delete.return_value.status_code = 200
    alerts.delete_alert("a", False, "")
    alerts.session.delete.assert_called_once()


def test_delete_alert_delete_all(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    alerts.session = MagicMock()
    alerts.fetch_alerts_data = MagicMock(return_value=[{"id": "a"}, {"id": "b"}])  # type: ignore
    alerts.session.delete.return_value.status_code = 200
    alerts.delete_alert("", True, "")
    assert alerts.session.delete.call_count == 2


def test_delete_alert_group_filter(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    alerts.session = MagicMock()
    payloads = [
        {"id": "x", "analytic": {"plugin_id": "DataLatencyAlertingETL3"}},
        {"id": "y", "analytic": {"plugin_id": "SPC"}},
    ]
    alerts.fetch_alerts_data = MagicMock(return_value=payloads)  # type: ignore
    alerts.session.delete.return_value.status_code = 200
    alerts.delete_alert("", False, "data_latency")
    # Only one matching id should be deleted
    assert alerts.session.delete.call_count == 1


def test_convert_str_to_dict_and_reconstruct_json(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    df = pd.DataFrame([
        {"simple": "1", "nested": "{'a': 1}", "listv": "[1,2]"}
    ])
    converted = alerts.convert_str_to_dict(df.copy())
    assert isinstance(converted.loc[0, "nested"], dict)
    assert isinstance(converted.loc[0, "listv"], list)
    # reconstruct
    df2 = pd.DataFrame([
        {"a___b": 1, "c": 2}
    ])
    obj = alerts.reconstruct_json(df2)
    assert obj == [{"a": {"b": 1}, "c": 2}]


def test_remove_nan_keys_handles_dict_list_and_ndarray(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    data = {"a": np.nan, "b": [1, np.nan], "c": np.array([1, np.nan, 2])}
    cleaned = alerts.remove_nan_keys(data)
    assert "a" not in cleaned
    assert cleaned["b"] == [1]
    assert list(cleaned["c"]) == [1, 2]


def test_create_alert_posts_payloads(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    alerts.session = MagicMock()
    alerts.session.post.return_value.status_code = 200
    df = pd.DataFrame([
        {"display_name": "A"},
        {"display_name": "B"},
    ])
    alerts.create_alert("", df)
    assert alerts.session.post.call_count == 2


def test_create_alert_filters_by_group(get_session: Any) -> None:
    alerts = _make_alerts(get_session)
    alerts.session = MagicMock()
    alerts.session.post.return_value.status_code = 200
    df = pd.DataFrame([
        {"display_name": "match", "analytic___plugin_id": "DataLatencyAlertingETL3"},
        {"display_name": "skip", "analytic___plugin_id": "SPC"},
    ])
    alerts.create_alert("data_latency", df)
    assert alerts.session.post.call_count == 1
