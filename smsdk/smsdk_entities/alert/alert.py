import json
from pandas import json_normalize
import copy
from typing import List
import pandas as pd
import ast

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
    def update_alert_payload(self,payload, updates):
        """
        Update the alert payload with new values provided in the updates dictionary.

        :param payload: dict, the original payload
        :param updates: dict, fields to be updated in the payload
        :return: dict, updated payload
        """
        updated_payload = copy.deepcopy(payload)  # Avoid modifying the original payload

        if "display_name" in updates:
            updated_payload["display_name"] = updates["display_name"]

        if "email_list" in updates:
            if updates.get("extend_lists", False):
                updated_payload["notification"]["backend"]["email"]["email_list"].extend(updates["email_list"])
            else:
                updated_payload["notification"]["backend"]["email"]["email_list"] = updates["email_list"]

        if "interval" in updates:
            updated_payload["trigger"]["schedule"]["interval"] = updates["interval"]
            updated_payload["analytic"]["plugin_parameters"]["alert_config"]["max_latency"] = updates["interval"]

        if "max_latency" in updates:
            updated_payload["analytic"]["plugin_parameters"]["alert_config"]["max_latency"] = updates["max_latency"]

        if "white_list" in updates:
            if updates.get("extend_lists", False):
                updated_payload["analytic"]["plugin_parameters"]["alert_config"]["white_list"].extend(
                    updates["white_list"])
            else:
                updated_payload["analytic"]["plugin_parameters"]["alert_config"]["white_list"] = updates["white_list"]

        if "black_list" in updates:
            if updates.get("extend_lists", False):
                updated_payload["analytic"]["plugin_parameters"]["alert_config"]["black_list"].extend(
                    updates["black_list"])
            else:
                updated_payload["analytic"]["plugin_parameters"]["alert_config"]["black_list"] = updates["black_list"]

        keys_to_remove = [
            "incident_total", "id", "created_by", "system_fixture", "audit_keys", "tombstone_epoch",
            "tombstone", "version", "updatelocation", "localtz", "updatetime", "capturetime_epoch", "capturetime"
        ]
        for key in keys_to_remove:
            updated_payload.pop(key, None)

        return updated_payload


    @mod_util
    def get_utilities(self, *args, **kwargs) -> List:
        """
        Get the list of registered utilites by name
        """
        return [*self.mod_util.all]

    @mod_util
    def get_alert_config(self,alert_id):
        url = "{}{}{}".format(self.base_url, '/v1/obj/alert_config/',alert_id)
        response = self.session.get(url)
        if response.status_code in [200, 201]:
            alert_config = response.json()
            return alert_config
        else:
            print(f"\033[91m{response.text}\033[0m")
            return None

    @mod_util
    def get_filtered_alerts_by_group(self,alerts,alert_group):
        mapping = {"kpi": "KPIAlerting",
                   "data_latency": "DataLatencyAlertingETL3",
                   "spc": "SPCXBarRControlChartTable"}
        alert_plugin_id = mapping.get(alert_group.lower(), None)
        alerts = [data for data in alerts if data["analytic"].get("plugin_id") == alert_plugin_id]
        return alerts

    @mod_util
    def update_alert(self,alert_id,updated_params):
        original_alert=self.get_alert_config(alert_id)
        if updated_params:
            updated_payload=self.update_alert_payload(original_alert,updated_params)
            url = "{}{}{}".format(self.base_url, '/v1/obj/alert_config/',alert_id)
            response = self.session.put(url,json=updated_payload)
            if response.status_code in [200,201]:
                print(f"\033[92mSuccessfully updated alert with id \033[0m`{alert_id}`.")
            else:
                print(f"\033[91m{response.text}\033[0m")
        else:
            print("Please enter params to be updated in dict format for `updated_params`")
    @mod_util
    def fetch_alerts_data(self):
        url = "{}{}".format(self.base_url, '/v1/obj/alert_config')
        response = self.session.get(url)
        if response.status_code in [200, 201]:
            alerts = response.json()['objects']
            return alerts
        else:
            print(f"\033[91m{response.text}\033[0m")
            return []
    @mod_util
    def list_alerts(self,alert_type):
        """

        """
        mapping = {"kpi": "KPIAlerting",
                   "data_latency": "DataLatencyAlertingETL3",
                   "spc": "SPCXBarRControlChartTable"}
        alert_plugin_id = mapping.get(alert_type.lower(), None)
        alerts=self.fetch_alerts_data()
        if alerts:
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
            alert_dataframes=pd.DataFrame(transformed_data)
            return alert_dataframes
        return None

    @mod_util
    def get_alert_dataframe(self, alert_type):
        """

        """
        alerts = self.fetch_alerts_data()
        alert_ids = [data['id'] for data in alerts]

        if alert_type:
            alerts = self.get_filtered_alerts_by_group(alerts,alert_type)
            alert_ids=[data['id'] for data in alerts ]
        if alert_ids:
            alert_data=[]
            for id in alert_ids:
                config = self.get_alert_config(id)
                if config:
                    keys_to_remove = [
                        "incident_total", "id", "created_by", "system_fixture", "audit_keys", "tombstone_epoch",
                        "tombstone", "version", "updatelocation", "localtz", "updatetime", "capturetime_epoch",
                        "capturetime"
                    ]
                    for key in keys_to_remove:
                        config.pop(key, None)

                    alert_data.append(config)
            if alert_data:
                alerts_df = json_normalize(alert_data, sep='___', max_level=2)
                return alerts_df
        return None


    @mod_util
    def delete_alert(self,alert_id,delete_all,alert_group):
        alerts = self.fetch_alerts_data()
        alerts_ids_dict ={alert['id']:alert for alert in alerts}
        if alert_id:
            if alert_id not in alerts_ids_dict:
                print("\033[91mInvalid alert id.. not found in existing alerts\033[0m")
            else:
                _response = self.session.delete(f"{self.base_url}/v1/obj/alert_config/{alert_id}")
                if _response.status_code in [200, 201]:
                    print(f"Successfully deleted alert with id : {alert_id}")
                else:
                    print(f"\033[91mFailed to delete alert with id:\033[0m {alert_id} \033[91mdue to:\033[0m {_response.text}")
        if delete_all:
            for alert_id in alerts_ids_dict:
                _response = self.session.delete(f"{self.base_url}/v1/obj/alert_config/{alert_id}")
                if _response.status_code in [200,201]:
                    print(f"\033[92mSuccessfully deleted alert with id :\033[0m `{alert_id}`")
                else:
                    print(f"\033[91mFailed to delete alert with id:\033[0m {alert_id} \033[91mdue to:\033[0m {_response.text}")
        if alert_group:
            alerts=self.get_filtered_alerts_by_group(alerts,alert_group)
            alert_ids = [data['id'] for data in alerts]
            for alert_id in alert_ids:
                _response = self.session.delete(f"{self.base_url}/v1/obj/alert_config/{alert_id}")
                if _response.status_code in [200, 201]:
                    print(f"\033[92mSuccessfully deleted alert with id :\033[0m `{alert_id}`")
                else:
                    print(
                        f"\033[91mFailed to delete alert with id:\033[0m {alert_id} \033[91mdue to:\033[0m {_response.text}")

    # Convert string representations of dictionaries back to actual dictionaries
    @mod_util
    def convert_str_to_dict(self,df):
        for col in df.columns:
            df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) and (x.startswith("{") or x.startswith("[")) else x)
        return df

    # Apply conversion
    # Convert back to nested dictionary
    @mod_util
    def reconstruct_json(self,df):
        result = []
        for _, row in df.iterrows():
            item = {}
            for col, value in row.items():
                keys = col.split("___")  # Reverse the flattening
                temp = item
                for key in keys[:-1]:  # Traverse nested keys
                    temp = temp.setdefault(key, {})
                temp[keys[-1]] = value
            result.append(item)
        return result

    # Get back the nested JSON
    @mod_util
    def remove_nan_keys(self,d):
        """Recursively remove keys with NaN values from a nested dictionary."""
        if isinstance(d, dict):
            return {k: self.remove_nan_keys(v) for k, v in d.items() if not (isinstance(v, (float, int)) and pd.isna(v))}
        elif isinstance(d, list):
            return [self.remove_nan_keys(v) for v in d if not (isinstance(v, (float, int)) and pd.isna(v))]
        elif isinstance(d, np.ndarray):
            return np.array([self.remove_nan_keys(v) for v in d if not (isinstance(v, (float, int)) and pd.isna(v))])
        else:
            return d
    @mod_util
    def create_alert(self,alert_type,dataframe):
        dataframe = self.convert_str_to_dict(dataframe)
        json_data = self.reconstruct_json(dataframe)
        if alert_type:
            json_data = self.get_filtered_alerts_by_group(json_data,alert_type)
        if json_data:
            for new_alert in json_data:
                new_alert=self.remove_nan_keys(new_alert)
                url = "{}{}".format(self.base_url, '/v1/obj/alert_config')
                response = self.session.post(url,json=new_alert)
                if response.status_code in [200,201]:
                    print(f"\033[92mSuccessfully added new alert {new_alert['display_name']}\033[0m")
                else:
                    print(f"\033[91m{response.text}\033[92m")