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
import pytz
import numpy as np

import logging

log = logging.getLogger(__name__)

ENDPOINTS = json.loads(pkg_resources.read_text(config, "api_endpoints.json"))


@smsdkentities.register("cycle_v1")
class Cycle(SmsdkEntities, MaSession):
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
    def get_cycles(self, *args, **kwargs):
        """
        Utility function to get the cycles
        from MA API
        Recommend to use 'enable_pagination':True for larger datasets
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["Cycle"]["url_v1"])

        # if 'machine__source' not in kwargs and 'machine__source__in' not in kwargs:
        #     log.warn('Machine source not specified.')
        #     return []

        if "/api/cycle" in url:
            records = self._get_records(url, **kwargs)
        else:
            kwargs = self.modify_input_params(**kwargs)
            records = self._get_records_v1(url, **kwargs)

        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records

    def modify_input_params(self, **kwargs):
        # Special handling for EF type names
        machine = kwargs.get("machine__source", "")

        if machine[0] == "'":
            machine = machine[1:-1]

        machine_type = kwargs.get("machine_type", "")
        if machine_type[0] == "'":
            machine_type = machine_type[1:-1]

        new_kwargs = {}
        relative_timedelta_days = kwargs.get("relative_timedelta_days", 7)
        etime = datetime.now()
        stime = etime - timedelta(days=relative_timedelta_days)
        new_kwargs["asset_selection"] = {
            "machine_source": machine,
            "machine_type": machine_type,
        }

        time_selection = {
            'time_zone': kwargs.get('output_tz', 'UTC'),
            'time_type': 'absolute'
        }
        new_kwargs['time_selection'] = time_selection
        try:
            del kwargs['output_tz']
            del kwargs['relative_timedelta_days']
        except:
            pass

        start_key, end_key = self.get_starttime_endtime_keys(**kwargs)

        # https://37-60546292-gh.circle-artifacts.com/0/build/html/web_api/v1/datatab/index.html#get--v1-datatab-cycle
        where = []

        timezone = pytz.timezone(time_selection['time_zone'])

        if start_key:
            starttime = kwargs.get(start_key, "") if start_key else stime
            # where.append(
            #     {
            #         "name": start_key.split("__")[0],
            #         "op": start_key.split("__")[-1],
            #         "value": starttime.isoformat(),
            #     }
            # )
        else:
            print("No start_key found, using relative_timedelta_days as: ", relative_timedelta_days, " and starttime is: ", stime)
            starttime = stime

        starttime = timezone.localize(starttime)
        starttime = starttime.astimezone(pytz.utc)
        new_kwargs['time_selection']['start_time'] = starttime.replace(tzinfo=None).isoformat("T", "milliseconds")+'Z'

        if end_key:
            endtime = kwargs.get(end_key, "") if end_key else etime
            # where.append(
            #     {
            #         "name": end_key.split("__")[0],
            #         "op": end_key.split("__")[-1],
            #         "value": endtime.isoformat(),
            #     }
            # )
        else:
            print("No end_key found, using relative_timedelta_days as: ", relative_timedelta_days, " and end_time is: ", etime)
            endtime = etime

        end_time = timezone.localize(endtime)
        end_time = end_time.astimezone(pytz.utc)
        new_kwargs['time_selection']['end_time'] = end_time.replace(tzinfo=None).isoformat("T", "milliseconds")+'Z'

        print("time_selection: ", new_kwargs['time_selection'])

        for kw in kwargs:
            if (
                kw[0] != "_"
                and "machine_type" not in kw
                and "Machine" not in kw
                and "machine__source" not in kw
                and "End Time" not in kw
                and "endtime" not in kw
                and "Start Time" not in kw
                and "starttime" not in kw
            ):
                if "__" not in kw:
                    where.append({"name": kw, "op": "eq", "value": kwargs[kw]})
                else:
                    key = "__".join(kw.split("__")[:-1])
                    op = kw.split("__")[-1]

                    if op == "val":
                        op = "eq"
                        key += "__val"

                    if op != "exists":
                        where.append({"name": key, "op": op, "value": kwargs[kw]})
                    else:
                        if kwargs[kw]:
                            where.append({"name": key, "op": "ne", "value": None})
                        else:
                            where.append({"name": key, "op": "eq", "value": None})

        new_kwargs["select"] = [{"name": i} for i in kwargs["_only"]]
        new_kwargs["offset"] = kwargs.get("_offset", 0)
        new_kwargs["limit"] = kwargs.get("_limit", np.Inf)
        new_kwargs["where"] = where

        if kwargs.get("_order_by", ""):
            order_key = kwargs["_order_by"].replace("_epoch", "")
            if order_key.startswith("-"):
                order_type = "desc"
                order_key = order_key[1:]
            else:
                order_type = "asc"
            new_kwargs["order_by"] = [{"name": order_key, "order": order_type}]

        return new_kwargs
