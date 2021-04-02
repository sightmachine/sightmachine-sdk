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


@smsdkentities.register("downtime_v1")
class Downtime(SmsdkEntities, MaSession):
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
    def get_downtime(self, *args, **kwargs):
        """
        Utility function to get the downtimes
        from the ma downtime API
        Recommend to use 'enable_pagination':True for larger datasets
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["Downtime"]["url_v1"])

        self.session.headers = self.modify_header_style(url, self.session.headers)

        if '/api/downtime' in url:
            records = self._get_records(url, **kwargs)
        else:
            kwargs = self.modify_input_params(**kwargs)
            records = self._get_records_v1(url, **kwargs)

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
        new_kwargs['select'] = [{'name': i} for i in kwargs['_only']]
        new_kwargs['offset'] = kwargs.get('_offset', 0)
        new_kwargs['limit'] = kwargs.get('_limit', np.Inf)

        return new_kwargs
