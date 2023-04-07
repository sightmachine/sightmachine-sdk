import json
from datetime import datetime, timedelta
from typing import List

import numpy as np

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from smsdk.tool_register import SmsdkEntities, smsdkentities
from smsdk.utils import module_utility
from smsdk import config
from smsdk.ma_session import MaSession

import logging

log = logging.getLogger(__name__)

ENDPOINTS = json.loads(pkg_resources.read_text(config, "api_endpoints.json"))


@smsdkentities.register("kpi")
class KPI(SmsdkEntities, MaSession):
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
    def get_kpis(self, *args, **kwargs):
        """
        Returns a list of all KPIs
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["Assets"]["url"])
        records = self._get_records_v1(url, method="get", **kwargs)[0]["kpi"]

        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records

    @mod_util
    def get_kpis_for_asset(self, *args, **kwargs):
        """
        Takes an asset selection
        returns a list of KPIs avaible to that asset
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["KPI"]["availible_kpis_for_asset"])
        records = self._get_records_v1(url, **kwargs)

        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records

    @mod_util
    def get_kpi_data_viz(self, *args, **kwargs):
        """
        Takes a Data Viz query for the KPI model
        Returns Data Viz info for that query
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["DataViz"]["task"])
        kwargs["model"] = "kpi"
        records = self._complete_async_task(url, **kwargs)

        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records
