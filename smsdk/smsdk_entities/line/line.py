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


@smsdkentities.register("line")
class Line(SmsdkEntities, MaSession):
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
    def get_lines(self, *args, **kwargs):
        """
        Returns a list of all lines
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["Assets"]["url"])
        records = self._get_records_v1(url, method="get", **kwargs)[0]["line"]

        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records

    @mod_util
    def get_line_data(self, limit=400, offset=0, *args, **kwargs):
        """
        Returns a list of all lines
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["Line"]["url"])
        records = self._get_records_v1(
            url, method="post", limit=limit, offset=offset, **kwargs
        )

        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records
