import json
from datetime import datetime, timedelta
from typing import List
import uuid

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


@smsdkentities.register("dataViz")
class DataViz(SmsdkEntities, MaSession):
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
    def create_share_link(self, asset, chartType, yAxis, xAxis, model, *args, **kwargs):
        """
        Creates a share link
        """
        url = "{}{}".format(self.base_url, ENDPOINTS['DataViz']['share_link'])
        url_params= kwargs
        url_params['state_hash'] = str(uuid.uuid4())[:8]
        url_params['context'] = "/analysis/datavis"
        url_params['state'] = {
            'dataModel': model,
            'asset': asset,
            'chartType': chartType,
            'xAxis': xAxis,
            # xAxis: {
            #     'id': "endtime",
            #     'title': "Time",
            # },
            # 'yAxis':
            # {
            #         "id": "stats__0_BM 008: Cans Out__val",
            #         "title": "0_BM 008: Cans Out",
            # }
            # 'yAxisMulti':
            # [
            #     {
            #         "id": "stats__0_BM 008: Cans Out__val",
            #         "title": "0_BM 008: Cans Out",
            #     }
            # ]
        }
        if isinstance(yAxis, List):
             url_params['state']['yAxisMulti'] = yAxis
        else:
            url_params['state']['yAxis'] = yAxis
        response = getattr(self.session, 'post')(
                    url, json=url_params
                )
        return "{}/#/analysis/datavis/s/{}".format(self.base_url, response.json()['state_hash'])