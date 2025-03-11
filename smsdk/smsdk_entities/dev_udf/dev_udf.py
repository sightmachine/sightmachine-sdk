import time
from typing import List, Any, Dict, Union, Tuple
from bs4 import BeautifulSoup
import json
import importlib.resources as pkg_resources
from smsdk.tool_register import SmsdkEntities, smsdkentities
from smsdk.utils import module_utility
from smsdk import config
from smsdk.ma_session import MaSession
import logging

log = logging.getLogger(__name__)

ENDPOINTS = json.loads(pkg_resources.read_text(config, "api_endpoints.json"))


@smsdkentities.register("dev_udf")
class UDFData(SmsdkEntities, MaSession):
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
        self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]
    ) -> List[Any]:
        return [*self.mod_util.all]

    @mod_util
    def get_list_of_udf(self) -> List[Any]:
        """
        Utility function to get list of UDF present in dev tool
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["UDF_dev"]["list_url"])
        response = self.session.get(url).json()
        list_of_udfs = [udf["name"] for udf in response]
        return list_of_udfs

    @mod_util
    def get_udf_data(self, udf_name: str, params: Dict[str, Any]) -> List[Any]:
        """
        Utility function to get the data after executing udf notebook
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["UDF_dev"]["url"])
        payload: Dict[str, Any] = {"name": udf_name}

        if params:
            if isinstance(params, dict):
                payload["parameters"] = params
            else:
                raise TypeError("Expected 'params' to be a dictionary or None.")

        results = self.session.post(url, json=payload)
        time.sleep(10)

        async_task_id: str = results.json().get("response").get("task_id")

        results = self.session.get(url + "/" + async_task_id).json()
        time.sleep(10)

        response = results.get("response")
        if (
            not response
            or "meta" not in response
            or not isinstance(response["meta"], list)
        ):
            raise ValueError("Response does not contain a valid 'meta' structure.")

        meta = response["meta"]
        if not meta or not isinstance(meta[0], dict) or "data" not in meta[0]:
            raise ValueError("Meta does not contain a valid 'data' key.")

        data: List[Any] = meta[0]["data"]
        return data
