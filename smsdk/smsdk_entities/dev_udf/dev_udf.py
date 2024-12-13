import time
from typing import List
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

    def __init__(self, session, base_url) -> None:
        self.session = session
        self.base_url = base_url

    @mod_util
    def get_utilities(self, *args, **kwargs) -> List:
        return [*self.mod_util.all]

    def get_list_of_udf(self):
        """
        Utility function to get list of UDF present in dev tool
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["UDF_dev"]["list_url"])
        html_content = self.session.get(url).text
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table")
        rows = table.find("tbody").find_all("tr")
        list_of_udfs = [row.find_all("td")[0].text for row in rows]
        return list_of_udfs

    @mod_util
    def get_udf_data(self, udf_name, params) -> List:
        """
        Utility function to get the data after executing udf notebook
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["UDF_dev"]["url"])
        payload = {"name": udf_name}
        if params:
            payload["parameters"] = params
        results = self.session.post(url, json=payload)
        time.sleep(10)
        async_task_id = results.json().get("response").get("task_id")
        results = self.session.get(url + "/" + async_task_id).json()
        time.sleep(10)
        data = results.get("response").get("meta")[0].get("data")
        return data
