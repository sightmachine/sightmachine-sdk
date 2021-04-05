import json
from typing import List

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from smsdk.tool_register import SmsdkEntities, smsdkentities
from smsdk.utils import module_utility
from smsdk import config
from smsdk.ma_session import MaSession
from datetime import datetime, timedelta
import numpy as np

import logging

log = logging.getLogger(__name__)

ENDPOINTS = json.loads(pkg_resources.read_text(config, "api_endpoints.json"))


@smsdkentities.register("dataviz_cycle")
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
    def cycle_count(self, *args, **kwargs):
        url = "{}{}".format(self.base_url, ENDPOINTS["DataViz"]["async"])
        resp_url = "{}{}".format(self.base_url, ENDPOINTS["DataViz"]["async_resp"])

        self.session.headers = self.modify_header_style(url, self.session.headers)

        async_task_id = self._get_task_id(url, **kwargs)

        WAIT_TIME = 0.5
        from time import sleep

        while True:
            sleep(WAIT_TIME)
            response = self._get_task_response(resp_url, task_id=async_task_id, method="get")
            if response['state'] == "SUCCESS":
                response = response['meta']
                break
        """
        SAMPLE results
         'results': [{'i_vals': {'endtime': {'i_pos': 0,
                                             'bin_no': 0,
                                             'bin_min': '2021-04-05T00:00:00+05:30',
                                             'bin_max': '2021-04-05T00:00:00+05:30',
                                             'bin_avg': '2021-04-05T00:00:00+05:30'},
                                 'machine__source': {'i_pos': 1,
                                                     'bin_no': 0,
                                                     'bin_min': 'F1_010_CupPress_1',
                                                     'bin_max': 'F1_010_CupPress_1',
                                                     'bin_avg': 'F1_010_CupPress_1'}},
                      'd_vals': {'cycle_count': {'sum': 911}},
                      '_count': 911},
                     {'i_vals': {'endtime': {'i_pos': 0,
                                             'bin_no': 1,
                                             'bin_min': '2021-04-05T00:00:00+05:30',
                                             'bin_max': '2021-04-05T00:00:00+05:30',
                                             'bin_avg': '2021-04-05T00:00:00+05:30'},
                                 'machine__source': {'i_pos': 1,
                                                     'bin_no': 1,
                                                     'bin_min': 'F2_010_CupPress_1',
                                                     'bin_max': 'F2_010_CupPress_1',
                                                     'bin_avg': 'F2_010_CupPress_1'}},
                      'd_vals': {'cycle_count': {'sum': 920}},
                      '_count': 920},
                     {'i_vals': {'endtime': {'i_pos': 0,
                                             'bin_no': 2,
                                             'bin_min': '2021-04-05T00:00:00+05:30',
                                             'bin_max': '2021-04-05T00:00:00+05:30',
                                             'bin_avg': '2021-04-05T00:00:00+05:30'},
                                 'machine__source': {'i_pos': 1,
                                                     'bin_no': 2,
                                                     'bin_min': 'F3_010_CupPress_1',
                                                     'bin_max': 'F3_010_CupPress_1',
                                                     'bin_avg': 'F3_010_CupPress_1'}},
                      'd_vals': {'cycle_count': {'sum': 913}},
                      '_count': 913}]}
        """

        try:
            records = [{'endtime': i['i_vals']['endtime']['bin_avg'], 'source': i['i_vals']['machine__source']['bin_avg'],
                        "rows": i['_count']} for i in response['results']]
        except Exception as e:
            logging.warning(response)
            raise ValueError("Error - {}".format(repr(e)))

        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records

    def modify_input_params(self, **kwargs):
        new_kwargs = {}
        etime = datetime.now()
        stime = etime - timedelta(days=1)
        new_kwargs['asset_selection'] = {
            "machine_source": [kwargs.get('machine__source', '')],
            "machine_type": kwargs.get('machine_type', '')
        }

        new_kwargs["time_selection"] = {
            "time_type": "absolute",
            "start_time": kwargs.get('endtime__gte', stime).isoformat(),
            "end_time": kwargs.get('endtime__lte', etime).isoformat(),
            "time_zone": "UTC"
        }

        new_kwargs["time_selection"] = {
            "time_type": "relative",
            "relative_start": 1,
            "relative_unit": "week",
            "ctime_tz": "Asia/Calcutta"
        }

        new_kwargs['select'] = [{'name': i} for i in kwargs['_only']]
        new_kwargs['offset'] = kwargs.get('_offset', 0)
        new_kwargs['limit'] = kwargs.get('_limit', np.Inf)

        return new_kwargs
