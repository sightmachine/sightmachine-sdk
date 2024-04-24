from typing import List
import json

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


@smsdkentities.register("dashboard_v1")
class DashboardData(SmsdkEntities, MaSession):
    # Decorator to register a function as utility
    # Only the registered utilites would be accessible
    # to outside world via client.get_data()
    mod_util = module_utility()
    log = log

    def __init__(self, session, base_url) -> None:
        self.session = session
        self.base_url = base_url

    @mod_util
    def get_utilities(self, *args, **kwargs) -> List:
        return [*self.mod_util.all]

    @mod_util
    def get_dashboards(self):
        """
        Utility function to get the machine types
        from the ma machine API
        Recommend to use 'enable_pagination':True for larger datasets
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["Dashboard"]["url_v1"])
        log.warning(f"=========={url}==============")

        records = self._get_records_v1(url, method="get", results_under="objects")
        records_new = self._get_records(url, method="get")
        log.warning(f"=========={records_new}==============")

        if records_new:
            print("")
            return records_new
        elif not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records
