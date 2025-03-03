import unittest
from unittest.mock import patch, MagicMock
import sys
print("===================",sys.path)

# Check if smsdk can be imported
import smsdk

from smsdk.smsdk_entities.alert.alert import *




class TestAlertFunctions(unittest.TestCase):
    def test_update_alert_payload(self):
        payload = {"id": 1, "status": "active"}
        updates = {"status": "resolved"}
        expected = {"id": 1, "status": "resolved"}
        self.assertEqual(update_alert_payload(payload, updates), expected)

    def test_get_updated_alert(self):
        alert = {"id": 1, "status": "active"}
        updates = {"status": "resolved"}
        expected = {"id": 1, "status": "resolved"}
        self.assertEqual(get_updated_alert(alert, updates), expected)

    def test_get_filtered_alerts_by_group(self):
        alerts = [
            {"id": 1, "group": "A"},
            {"id": 2, "group": "B"},
            {"id": 3, "group": "A"},
        ]
        expected = [{"id": 1, "group": "A"}, {"id": 3, "group": "A"}]
        self.assertEqual(get_filtered_alerts_by_group(alerts, "A"), expected)

    @patch("smsdk.smsdk_entities.alert.alert.get_alert_config")
    def test_get_alert_config(self, mock_get_alert_config):
        mock_get_alert_config.return_value = {"config": "sample"}
        self.assertEqual(get_alert_config(), {"config": "sample"})

    @patch("smsdk.smsdk_entities.alert.alert.update_alert")
    def test_update_alert(self, mock_update_alert):
        mock_update_alert.return_value = True
        self.assertTrue(update_alert(1, {"status": "resolved"}))

    @patch("smsdk.smsdk_entities.alert.alert.update_alert_group")
    def test_update_alert_group(self, mock_update_alert_group):
        mock_update_alert_group.return_value = True
        self.assertTrue(update_alert_group("A", {"priority": "high"}))

    @patch("smsdk.smsdk_entities.alert.alert.fetch_alerts_data")
    def test_fetch_alerts_data(self, mock_fetch_alerts_data):
        mock_fetch_alerts_data.return_value = [{"id": 1, "status": "active"}]
        self.assertEqual(fetch_alerts_data(), [{"id": 1, "status": "active"}])

    @patch("smsdk.smsdk_entities.alert.alert.delete_alert")
    def test_delete_alert(self, mock_delete_alert):
        mock_delete_alert.return_value = True
        self.assertTrue(delete_alert(1))

    @patch("smsdk.smsdk_entities.alert.alert.list_alerts")
    def test_list_alerts(self, mock_list_alerts):
        mock_list_alerts.return_value = ["alert1", "alert2"]
        self.assertEqual(list_alerts(), ["alert1", "alert2"])

    @patch("smsdk.smsdk_entities.alert.alert.get_alert_dataframe")
    def test_get_alert_dataframe(self, mock_get_alert_dataframe):
        mock_df = MagicMock()
        mock_get_alert_dataframe.return_value = mock_df
        self.assertEqual(get_alert_dataframe(), mock_df)

