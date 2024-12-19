from typing import List, Any
import json

import importlib.resources as pkg_resources
from smsdk.tool_register import SmsdkEntities, smsdkentities
from smsdk.utils import module_utility
from smsdk import config
from smsdk.ma_session import MaSession
import logging

log = logging.getLogger(__name__)

ENDPOINTS = json.loads(pkg_resources.read_text(config, "api_endpoints.json"))


@smsdkentities.register("dashboard")
class DashboardData(SmsdkEntities, MaSession):
    # Decorator to register a function as utility
    # Only the registered utilites would be accessible
    # to outside world via client.get_data()
    mod_util = module_utility()
    log = log

    def __init__(self, session: Any, base_url: str) -> None:
        self.session = session
        self.base_url = base_url

    @mod_util
    def get_utilities(
        self, *args: tuple[Any, ...], **kwargs: dict[str, Any]
    ) -> List[Any]:
        return [*self.mod_util.all]

    @mod_util
    def get_dashboards(self, dashboard_id: str) -> List[Any]:
        """
        Utility function to get the panels data for dashboard
        """
        url = "{}{}{}".format(self.base_url, "/v1/obj/dashboard/", dashboard_id)
        panels: List[Any] = self._get_dashboard_panels(url, method="get")
        return panels
