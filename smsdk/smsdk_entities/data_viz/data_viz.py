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
    def create_share_link(self, *args, **kwargs):
        """
        Creates a share link
        """
        url = "{}{}".format(self.base_url, ENDPOINTS['DataViz']['share_link'])
        url_params= {}
        url_params['state_hash'] = str(uuid.uuid4())[:8]
        url_params['context'] = "/analysis/datavis"
        url_params['state'] = {
            'dataModel': 'cycle',
            'asset': {
                'machine_source': ["F1_010_BodyMaker_1"],
                'machine_type': ["Body_Maker"]
            },
            'chartType': 'line',
            'xAxis': {
                'data_type': "datetime",
                'id': "endtime",
                'isEnabled': True,
                'raw_data_field': "",
                'stream_types': [],
                'title': "Time",
                'type': "datetime",
                'unit': ""    
            },
            'yAxis': {
                "unit": "",
                "type": "discrete",
                "data_type": "int",
                "stream_types": [],
                "raw_data_field": "",
                "id": "cycle_count",
                "title": "Cycle Count",
                "isEnabled": True
            },
            'yAxisMulti':[
                {
                    "unit": "",
                    "type": "continuous",
                    "data_type": "float",
                    "stream_types": [],
                    "raw_data_field": "BM_008_COUT",
                    "formatting": {
                    "is_convertible": False
                    },
                    "annotations": {},
                    "ui_hidden": False,
                    "ui_hidden_machines": [],
                    "ui_hidden_facilities": [],
                    "machine_type": {
                    "id": "707d74d48771b446b9019b38",
                    "name": "Body_Maker",
                    "name_clean": "Body Maker"
                    },
                    "id": "stats__0_BM 008: Cans Out__val",
                    "title": "0_BM 008: Cans Out",
                    "isEnabled": True
                }
            ]
        }
        response = getattr(self.session, 'post')(
                    url, json=url_params
                )
        return "{}/#/analysis/datavis/s/{}".format(self.base_url, response.json()['state_hash'])