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


@smsdkentities.register("workspace")
class Workspace(SmsdkEntities, MaSession):
    # Decorator to register a function as utility
    # Only the registered utilites would be accessible
    # to outside world via client.get_data()
    mod_util = module_utility()

    def __init__(self, session, base_url) -> None:
        self.session = session
        self.base_url = base_url

    @mod_util
    def get_utilities(self, *args, **kwargs) -> List[Any]:
        """
        Get the list of registered utilites by name
        """
        return [*self.mod_util.all]

    @mod_util
    def get_cycles(self, *args, **kwargs) -> List[Any]:
        """
        Utility function to get the cycles
        from MA API
        Recommend to use 'enable_pagination':True for larger datasets
        """
        """
        Utility function to get the cycles
        from MA API
        Recommend to use 'enable_pagination':True for larger datasets
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["Cycle"]["alt_url"])

        if "machine__source" not in kwargs and "machine__source__in" not in kwargs:
            log.warn("Machine source not specified.")
            return []

        records = self._get_records(url, **kwargs)
        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records
