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

ENDPOINTS = json.loads(pkg_resources.read_text(config, "api_endpoints.json"))


@smsdkentities.register("part_v1")
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
        url = "{}{}".format(self.base_url, ENDPOINTS["Parts"]["url_v1"])

        self.session.headers = self.modify_header_style(url, self.session.headers)

        kwargs = self.modify_input_params(**kwargs)
        records = self._get_records_v1(url, **kwargs)
        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records

    def modify_input_params(self, **kwargs):
        new_kwargs = {}
        etime = datetime.now()
        stime = etime - timedelta(days=1)
        new_kwargs['asset_selection'] = {}

        start_key, end_key = self.get_starttime_endtime_keys(**kwargs)
        starttime = kwargs.get(start_key, "") if start_key else stime
        endtime = kwargs.get(end_key, "") if end_key else stime
        new_kwargs["time_selection"] = {
            "time_type": "absolute",
            "start_time": starttime.isoformat(),
            "end_time": endtime.isoformat(),
            "time_zone": "UTC"
        }

        new_kwargs["where"] = [{
            "name": "type__part_type",
            "op": "eq",
            "value": kwargs.get('type__part_type')
        }]

        new_kwargs['select'] = [{'name': i} for i in kwargs['_only']]
        new_kwargs['offset'] = kwargs.get('_offset', 0)
        new_kwargs['limit'] = kwargs.get('_limit', np.Inf)

        return new_kwargs
