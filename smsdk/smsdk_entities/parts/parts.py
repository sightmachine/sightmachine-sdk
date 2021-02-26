from typing import List
import json

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

ENDPOINTS = json.loads(pkg_resources.read_text(config, "api_endpoints.json"))

@smsdkentities.register("parts")
class Parts(SmsdkEntities, MaSession):
    # Decorator to register a function as utility
    # Only the registered utilites would be accessible
    # to outside world via client.get_data()
    mod_util = module_utility()

    def __init__(self, session, base_url) -> None:
        self.session = session
        self.base_url = base_url

    @mod_util
    def get_utilities(self, *args, **kwargs) -> List:
        return [*self.mod_util.all]

    @mod_util
    def get_parts(self, *args, **kwargs):
        """
        Utility function to get the parts
        from the ma machine API
        Recommend to use 'enable_pagination':True for larger datasets
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["Parts"]["url"])

        self.session.headers = self.modify_header_style(url, self.session.headers)

        records = self._get_records(url, **kwargs)
        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records

    @mod_util
    def get_part_schema(self, *args, **kwargs):
        """
        https://essex-torreon-spxim-97.sightmachine.io/v1/selector/datatab/part/pt_area_300/field?db_mode=sql&strip_aliases=false
        :return:
        """
        endpoint = f"/v1/selector/datatab/part/{kwargs.get('type__part_type')}/field?db_mode=sql&strip_aliases=false"
        url = "{}{}".format(self.base_url, endpoint)
        self.session.headers = self.modify_header_style(url, self.session.headers)
        records = self._get_records(url, **kwargs)
        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records
