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

import logging

log = logging.getLogger(__name__)

ENDPOINTS = json.loads(pkg_resources.read_text(config, "api_endpoints.json"))


@smsdkentities.register("cycle")
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
        url = "{}{}".format(self.base_url, ENDPOINTS["Cycle"]["url"])

        if 'machine__source' not in kwargs and 'machine__source__in' not in kwargs:
            log.warn('Machine source not specified.')
            return []

        self.session.headers = self.modify_header_style(url, self.session.headers)
        print(url)
        print(kwargs)
        if '/api/cycle' in url:
            records = self._get_records(url, **kwargs)
        else:
            kwargs = self.modify_input_params(**kwargs)
            records = self._get_records_v1(url, **kwargs)
        if not isinstance(records, List):
            raise ValueError("Error - {}".format(records))
        return records

    def modify_input_params(self, **kwargs):
        """
        x1 = {
        'machine__source': '200E_1',
        '_order_by': '-endtime_epoch',
        'endtime_epoch__gte': 1609459200000.0,
        'endtime_epoch__lte': 1609545600000.0,
        '_only': "['stats.Amp.val', 'stats.Audit.val', 'stats.Continuity.val', 'stats.Continuity_Amp.val', 'stats.Continuity_Voltage.val', 'stats.DeletedFlag.val', 'stats.Dept.val', 'stats.Dim1_Bare-Avg.val', 'stats.Dim1_OD-Avg.val', 'stats.Dim1_Overall Build.val', 'stats.Dim2_Bare-Avg.val', 'stats.Dim2_OD-Avg.val', 'stats.Dim2_Overall Build.val', 'stats.Dim3_Bare-Avg.val', 'stats.Dim3_OD-Avg.val', 'stats.Dim3_Overall Build.val', 'stats.Dim4_Bare-Avg.val', 'stats.Dim4_OD-Avg.val', 'stats.Dim4_Overall Build.val', 'stats.Employee.val', 'stats.Large_Bead_Threshold.val', 'stats.Large_Beads.val', 'stats.MaxVal.val', 'stats.MinVal.val', 'stats.NetWt.val', 'stats.Processed.val', 'stats.Qim_Bare-Avg.val', 'stats.Qim_OD-Avg.val', 'stats.Qim_Overall Build.val', 'stats.Small_Bead_Threshold.val', 'stats.Small_Beads.val', 'stats.Speed.val', 'stats.spool.val', 'stats.TgTVal.val', 'stats.Type.val', 'stats.ValAvg_Bare-Avg.val', 'stats.ValAvg_OD-Avg.val', 'stats.ValAvg_Overall Build.val', 'stats.ValueSFSraw.val', 'stats.reason.val', 'stats.reasonTop.val', 'stats.StdSpd.val', 'stats.current_location.val', 'stats.emailbead.val', 'stats.emailconti.val', 'stats.metal.val', 'stats.msgalarmbead.val', 'stats.net_wt.val', 'stats.nextspool.val', 'stats.pallet.val', 'machine.source', 'starttime', 'endtime', 'total', 'record_time', 'shift', 'output']"
    }


        x = {
            "asset_selection": {
                "machine_source": ["200E_1"],
                "machine_type": "mt_200e"
            },
            "time_selection": {
                "time_type": "absolute",
                "start_time": "2021-02-01T00:00:00.000Z",
                "end_time": "2021-02-02T23:59:59.999Z",
                "time_zone": "UTC"
            },
            "select": [{
                "name": "machine__source"
            }
            ],
            "db_mode": "sql",
            "offset": 0,
            "limit": 400
        }
        """
        new_kwargs = {}

        new_kwargs['asset_selection'] = {
            "machine_source": [kwargs.get('machine__source','')],
            "machine_type": "mt_200e"
        }

        return kwargs
