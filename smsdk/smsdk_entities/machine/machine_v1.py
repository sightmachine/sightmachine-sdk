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
from urllib.parse import urlencode, urlunparse

ENDPOINTS = json.loads(pkg_resources.read_text(config, "api_endpoints.json"))


@smsdkentities.register("machine_v1")
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
        url = "{}{}".format(self.base_url, ENDPOINTS["Machine"]["url_v1"])
        url = self.modify_query_params(url, kwargs)
        records = self._get_records_v1(
            url, method="get", results_under="objects", **kwargs
        )
        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records

    def get_type_from_machine_name(self, machine_source, *args, **kwargs):
        """
        Function that gives the name of a machine from it's type
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["Assets"]["url"])
        records = self._get_records_v1(url, method="get", **kwargs)[0]["machine"]
        machine_type = ""
        for record in records:
            if (
                record["name"] == machine_source
                or record["display_name"] == machine_source
            ):
                machine_type = record["type"]
        return machine_type

    def modify_query_params(self, url, kwargs):
        where = []
        order_by = []
        params = {}
        for key, value in kwargs.items():
            where_query = {}
            orderby_query = {}
            select_query = {}
            if not key.startswith("_"):
                where_query["name"] = key
                where_query["value"] = value
                where.append(where_query)
            elif key == "_order_by":
                orderby_query["name"] = (
                    value.replace("-", "") if value.startswith("-") else value
                )
                orderby_query["order"] = "desc" if value.startswith("-") else "asc"
                order_by.append(orderby_query)

        select = [{"name": i} for i in eval(kwargs.get("_only", "[]"))]
        if len(where) > 0:
            where = json.dumps(where, ensure_ascii=False)
            params["where"] = where
        if len(order_by) > 0:
            order_by = json.dumps(order_by, ensure_ascii=False)
            params["order_by"] = order_by
        if len(select) > 0:
            select = json.dumps(select, ensure_ascii=False)
            params["select"] = select

        if params:
            encoded_params = urlencode(params)
            url = urlunparse(("", "", url, "", encoded_params, ""))

        return url
