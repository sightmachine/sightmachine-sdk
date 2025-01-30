import json
from pandas import json_normalize

from typing import List

import pandas as pd

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from smsdk.tool_register import SmsdkEntities, smsdkentities
from smsdk.utils import module_utility
from smsdk import config
from smsdk.ma_session import MaSession
from datetime import datetime, timedelta
import numpy as np

import logging

log = logging.getLogger(__name__)

ENDPOINTS = json.loads(pkg_resources.read_text(config, "api_endpoints.json"))

try:
    NPINFINITY = np.Inf
except AttributeError:
    # numpy 2.0
    NPINFINITY = np.inf


@smsdkentities.register("alert")
class Alert(SmsdkEntities, MaSession):
    # Decorator to register a function as utility
    # Only the registered utilites would be accessible
    # to outside world via client.get_data()
    mod_util = module_utility()

    def __init__(self, session, base_url) -> None:
        self.session = session
        self.base_url = base_url

    @mod_util
    def get_utilities(self, *args, **kwargs) -> List:
        """
        Get the list of registered utilites by name
        """
        return [*self.mod_util.all]
    @mod_util
    def fetch_alerts_data(self):
        url = "{}{}".format(self.base_url, '/v1/obj/alert_config')
        response = self.session.get(url)
        if response.status_code in [200, 201]:
            alerts = response.json()['objects']
            return alerts
        else:
            print(response.text)
            return []
    @mod_util
    def list_alerts_df(self,alert_type):
        """

        """
        mapping = {"kpi": "KPIAlerting",
                   "data_latency": "DataLatencyAlertingETL3",
                   "spc": "SPCXBarRControlChartTable"}
        alert_plugin_id = mapping.get(alert_type.lower(), None)
        alerts=self.fetch_alerts_data()
        if alerts:
            alerts_df=json_normalize(alerts,sep='_')
            transformed_data=[]
            for data in alerts:
                try:
                    creator=f"{data['created_by']['metadata']['first_name']} {data['created_by']['metadata']['last_name']}"
                except:
                    creator='Undefined Undefined'
                status="Enabled" if data.get("enabled") else "Disabled"
                alert_type=data["analytic"].get("plugin_id")
                if alert_plugin_id is not None:
                    if alert_plugin_id != alert_type:
                        continue
                incident_count=data.get("incident_total")
                display_name=data.get("display_name").strip()
                t_data={
                "display_name":display_name,
                "analytic": alert_type,
                "Creator":creator,
                "status": status,
                "incident_count": incident_count
                }
                if display_name:
                    transformed_data.append(t_data)
            return alerts_df,pd.DataFrame(transformed_data)
        return None,None
    @mod_util
    def delete_alert(self,alert_id,delete_all):
        alerts = self.fetch_alerts_data()
        alerts_ids_dict ={alert['id']:alert for alert in alerts}
        if alert_id not in alerts_ids_dict:
            print("Invalid alert id.. not found in existing alerts")
        else:
            self.session.delete(f"{self.base_url}/v1/obj/alert_config/{alert_id}")
        if delete_all:
            for alert_id in alerts_ids_dict:
                _response = self.session.delete(f"{self.base_url}/v1/obj/alert_config/{alert_id}")
                if _response.status_code in [200,201]:
                    print(f"Successfully deleted alert with id : {alert_id}")
                else:
                    print(f"Failed to delete alert with id: {alert_id} due to: {_response.text}")
