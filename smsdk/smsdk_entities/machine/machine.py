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

ENDPOINTS = json.loads(pkg_resources.read_text(config, "api_endpoints.json"))

@smsdkentities.register("machine")
class Machine(SmsdkEntities, MaSession):
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
    def get_machines(self, *args, **kwargs):
        """
        Utility function to get the machines
        from the ma machine API
        Recommend to use 'enable_pagination':True for larger datasets
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["Machine"]["url"])

        records = self._get_records(url, **kwargs)
        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records
