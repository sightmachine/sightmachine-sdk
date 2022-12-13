from typing import List
import json
from datetime import datetime, timedelta

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources


import numpy as np

from smsdk.tool_register import SmsdkEntities, smsdkentities
from smsdk.utils import module_utility
from smsdk import config
from smsdk.ma_session import MaSession

ENDPOINTS = json.loads(pkg_resources.read_text(config, "api_endpoints.json"))

@smsdkentities.register("factory_v1")
class Factory(SmsdkEntities, MaSession):
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
    def get_factories(self, *args, **kwargs):
        """
        Utility function to get the machines
        from the ma machine API
        Recommend to use 'enable_pagination':True for larger datasets
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["Factory"]["url_v1"])
        
        kwargs = self.modify_input_params(**kwargs)
        records = self._get_records_mongo_v1(url, **kwargs)
        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records

    def modify_input_params(self, **kwargs):

    # :qparam cb: conditional Cache busting flag. If this is the only query
    # parameter set, return a 204 No Content response with an empty list.

    # :qparam list[dict] select: optional Query Modifier. Fields from data record to only return.
    # :qparam list[dict] where: optional Query Modifier. Conditions to filter data upon.
    # :qparam list[] group_by: optional Query Modifier.
    # :qparam list[dict] order_by: optional Query Modifier. Fields to sort data by.
    # :qparam int limit: optional Query Modifier. Limit number of objects returned. Default/Max is 2000. If the max is
    #     exceed, error returned.
    # :qparam int offset: optional Query Modifier. Number of results to skip before starting to return results.

    # :qparam int per_page: optional Query Modifier. Number of results to display per page

        
        # Special handling for EF type names
        machine = kwargs.get('machine__source', None)

        if machine and machine[0] == "'":
            machine = machine[1:-1]

        machine_type = kwargs.get('machine_type', None)
        if machine_type and machine_type[0] == "'":
            machine_type = machine_type[1:-1]

        new_kwargs = {}
        etime = datetime.now()
        stime = etime - timedelta(days=1)
        # new_kwargs['asset_selection'] = {
        #     "machine_source": machine,
        #     "machine_type": machine_type
        # }

        start_key, end_key = self.get_starttime_endtime_keys(**kwargs)

        # https://37-60546292-gh.circle-artifacts.com/0/build/html/web_api/v1/datatab/index.html#get--v1-datatab-cycle
        where = []
        if start_key:
            starttime = kwargs.get(start_key, "") if start_key else stime
            where.append({'name': start_key.split('__')[0], 'op': start_key.split('__')[-1], 'value': starttime.isoformat()})

        if end_key:
            endtime = kwargs.get(end_key, "") if end_key else stime
            where.append({'name': end_key.split('__')[0], 'op': end_key.split('__')[-1], 'value': endtime.isoformat()})

        if machine:
            where.append({'name': 'machine_source', 'op': 'eq', 'value': machine})

        if machine_type:
            where.append({'name': 'machine_type', 'op': 'eq', 'value': machine_type})

        for kw in kwargs:
            if kw[0] != '_' and 'machine_type' not in kw and 'Machine' not in kw and 'machine__source' not in kw and 'End Time' not in kw and 'endtime' not in kw and 'Start Time' not in kw and 'starttime' not in kw:
                if '__' not in kw:
                    where.append({'name': kw, 'op': 'eq', 'value': kwargs[kw]})
                else:
                    key = '__'.join(kw.split('__')[:-1])
                    op = kw.split('__')[-1]

                    if op == 'val':
                        op = 'eq'
                        key += '__val'

                    if op != 'exists':
                        where.append({'name': key, 'op': op, 'value': kwargs[kw]})
                    else:
                        if kwargs[kw]:
                            where.append({'name': key, 'op': 'ne', 'value': None})
                        else:
                            where.append({'name': key, 'op': 'eq', 'value': None})
        if kwargs.get('_only', None):
            new_kwargs['select'] = [{'name': i} for i in kwargs['_only']]
        new_kwargs['offset'] = kwargs.get('_offset', 0)
        new_kwargs['limit'] = kwargs.get('_limit', np.Inf)
        new_kwargs['where'] = where

        if kwargs.get("_order_by", ""):
            order_key = kwargs["_order_by"].replace("_epoch","")
            if order_key.startswith('-'):
                order_type = 'desc'
                order_key = order_key[1:]
            else:
                order_type = 'asc'
            new_kwargs['order_by'] = [{'name': order_key, 'order': order_type}]

        new_kwargs = {
            key: json.dumps(value)
            for key, value in new_kwargs.items()
        }
        return new_kwargs

