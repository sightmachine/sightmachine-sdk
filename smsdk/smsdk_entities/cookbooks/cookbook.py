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


@smsdkentities.register("cookbook")
class Cookbook(SmsdkEntities, MaSession):
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
    def get_cookbooks(self, *args, **kwargs):
        """
        Returns a list of all Cookbooks
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["Cookbook"]["get_cookbooks"])
        records = self._get_records_v1(
            url, method="get", results_under="objects", **kwargs
        )

        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records

    @mod_util
    def get_top_results(self, recipe_group_id, limit=10, *args, **kwargs):
        """
        Returns the top results from a recipe group
        """
        url = "{}{}".format(
            self.base_url,
            ENDPOINTS["Cookbook"]["top_results"].format(recipe_group_id, limit),
        )
        records = self._get_records_v1(url, method="get", results_under=None, **kwargs)

        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records[0]

    @mod_util
    def get_current_value(self, variables, minutes=1440, **kwargs):
        """
        Gets the current value of levers and constraints
        """
        kwargs["minutes"] = minutes
        kwargs["variables"] = variables
        url = "{}{}".format(self.base_url, ENDPOINTS["Cookbook"]["current_value"])
        records = self._get_records_v1(
            url, offset=None, limit=None, db_mode=None, **kwargs
        )

        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records
