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
from smsdk.utils import module_utility, check_kw
from smsdk import config
from smsdk.ma_session import MaSession

ENDPOINTS = json.loads(pkg_resources.read_text(config, "api_endpoints.json"))

@smsdkentities.register("machine_type_v1")
class MachineType(SmsdkEntities, MaSession):
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
    def get_machine_types(self, normalize, *args, **kwargs):
        """
        Utility function to get the machine types
        from the ma machine API
        Recommend to use 'enable_pagination':True for larger datasets
        """
        kwargs = self.modify_input_params(**kwargs)
        url = "{}{}".format(self.base_url, ENDPOINTS["MachineType"]["url_v1"])
        records = self._get_records_mongo_v1(url, normalize, **kwargs)
        # if not isinstance(records, List):
        #     raise ValueError("Error - {}".format(records))
        return records

    def modify_input_params(self, **kwargs):
        v1_params = ["cb", "select", "where", "group_by", "order_by", "limit", "offset", "per_page", "cursor"]

        list_of_operations = [
            'ne', 'lt', 'lte', 'gt', 'gte', 'not', 'in', 
            'nin', 'mod', 'all', 'exists', 'exact', 'iexact', 
            'contains', 'icontains', 'startswith', 'istartswith', 
            'endswith', 'iendswith', 'match',
        ]
        
        # Special handling for EF type names
        machine = kwargs.get('machine__source')
        machine = machine[1:-1] if machine and machine[0] == "'" else machine
            
        machine_type = kwargs.get('machine_type')
        machine_type = machine_type[1:-1] if machine_type and machine_type[0] == "'" else machine_type
            
        new_kwargs = {}
        etime = datetime.now()
        stime = etime - timedelta(days=1)

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
            if check_kw(kw) and kw not in v1_params:
                if '__' not in kw:
                    where.append({'name': kw, 'op': 'eq', 'value': kwargs[kw]})
                elif "__" in kw and kw.split("__")[-1] in list_of_operations:
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
                else:
                    where.append({'name': kw, 'op': 'eq', 'value': kwargs[kw]})
                    
            if kwargs.get('_only'):
                new_kwargs['select'] = [{'name': i} for i in kwargs['_only']]
            
            new_kwargs['offset'] = kwargs.get('_offset', kwargs.get('offset', 1))
            new_kwargs['limit'] = kwargs.get('_limit', kwargs.get('limit', np.Inf))
            new_kwargs['where'] = where

            for p in v1_params:
                if not new_kwargs.get(p) and kwargs.get(p):
                    new_kwargs[p] = kwargs.get(p)

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

