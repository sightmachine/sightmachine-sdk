import json
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
    def list_alerts_df(self,alert_type=''):
        """
        Utility function to get the cycles
        from MA API
        Recommend to use 'enable_pagination':True for larger datasets
        """
        url = "{}{}".format(self.base_url, '/v1/obj/alert_config')

        # if 'machine__source' not in kwargs and 'machine__source__in' not in kwargs:
        #     log.warn('Machine source not specified.')
        #     return []

        response = self.session.get(url)
        if response.status_code in [200,201]:
            alerts = response.json()['objects']
            alerts_df=pd.DataFrame(alerts)
            transformed_data=[]
            for _, data in alerts_df.iterrows():
                try:
                    creator=f"{data['created_by']['metadata']['first_name']} {data['created_by']['metadata']['last_name']}"
                except:
                    creator='Undefined Undefined'
                status="Enabled" if data.get("enabled") else "Disabled"
                type=data["analytic"].get("plugin_id")
                incident_count=data.get("incident_total")
                display_name=data.get("display_name").strip()
                t_data={
                "display_name":display_name,
                "Creator":creator,
                "status": status,
                "analytic": type,
                "incident_count": incident_count

                }
                if display_name:
                    transformed_data.append(t_data)
            return alerts_df,pd.DataFrame(transformed_data)
        return None,None
