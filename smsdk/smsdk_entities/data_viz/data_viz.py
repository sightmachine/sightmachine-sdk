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
    def create_share_link(
        self,
        asset,
        chartType,
        yAxis,
        xAxis,
        model,
        time_selection,
        are_line_params_available=False,
        *args,
        **kwargs
    ):
        """
        Creates a share link
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["DataViz"]["share_link"])
        url_params = {}
        url_params["state_hash"] = str(uuid.uuid4())[:8]
        url_params["context"] = "/analysis/datavis"
        try:
            url_params["in_use_workspace"] = self.session.headers["X-Sm-Workspace-Id"]
        except:
            pass
        if time_selection["time_type"] == "relative":
            dateRange = {
                "mode": "relative",
                "relativeAmount": time_selection["relative_start"],
                "relativeUnit": time_selection["relative_unit"],
                "selectedTimeZone": time_selection["ctime_tz"],
            }

        elif time_selection["time_type"] == "absolute":
            dateRange = {
                "mode": "absolute",
                "startDate": time_selection["start_time"],
                "endDate": time_selection["end_time"],
                "selectedTimeZone": time_selection["time_zone"],
            }
        url_params["state"] = {
            "dataModel": model,
            "asset": asset,
            "chartType": chartType,
            "xAxis": xAxis,
            "dateRange": dateRange,
        }
        url_params["state"].update(kwargs)
        if model == "line":
            if are_line_params_available:
                pass
            else:
                del url_params["state"]["asset"]
                url_params["state"]["lineProcess"] = {}
                if not isinstance(asset, List) and asset.get("assetOffsets"):
                    url_params["state"]["lineProcess"]["assetOffsets"] = asset.get(
                        "assetOffsets"
                    )
                if not isinstance(asset, List) and asset.get("assets"):
                    selectedMachines = []
                    for machine in asset["assets"]:
                        selectedMachines.append({"machineName": machine})
                    url_params["state"]["lineProcess"][
                        "selectedMachines"
                    ] = selectedMachines
                else:
                    selectedMachines = []
                    for machine in asset:
                        selectedMachines.append({"machineName": machine})
                    url_params["state"]["lineProcess"][
                        "selectedMachines"
                    ] = selectedMachines

                if xAxis.get("id") == "endtime":
                    url_params["state"]["lineXAxis"] = [
                        {"field": {"name": "offset_endtime", "type": "datetime"}}
                    ]
                else:
                    url_params["state"]["lineXAxis"] = xAxis
                if isinstance(yAxis, List):
                    lineYAxis = []
                    for y in yAxis:
                        lineYAxis.append(
                            {
                                "field": {
                                    "name": y.get("field"),
                                    "machine_type": {
                                        "name": y.get("machineType"),
                                    },
                                },
                                "machineName": y.get("machineName"),
                            }
                        )
                    url_params["state"]["lineYAxisMulti"] = lineYAxis

                else:
                    url_params["state"]["lineYAxisMulti"] = [
                        {
                            "field": {
                                "name": yAxis.get("field"),
                                "machine_type": {
                                    "name": yAxis.get("machineType"),
                                },
                            },
                            "machineName": yAxis.get("machineName"),
                        }
                    ]

        else:
            if isinstance(yAxis, List):
                url_params["state"]["yAxisMulti"] = yAxis
            else:
                url_params["state"]["yAxis"] = yAxis
        response = getattr(self.session, "post")(url, json=url_params)
        return "{}/#/analysis/datavis/s/{}".format(
            self.base_url, response.json()["state_hash"]
        )

    @mod_util
    def get_dashboard_widget_data(self, model, *args, **kwargs):
        """
        Takes a query params from the widget in dashboard
        Returns Data info for that query
        """
        is_analytics = False
        if model == "line":
            endpoint = ENDPOINTS["DataViz"]["line_task"]
        elif model == "cycle":
            endpoint = ENDPOINTS["DataViz"]["task"]
            kwargs["model"] = model
        else:
            endpoint = ENDPOINTS["DataViz"]["analytics_task"]
            kwargs["is_analytics"] = not is_analytics
            is_analytics = True
        url = "{}{}".format(self.base_url, endpoint)
        records = self._complete_async_task(url, **kwargs)

        if not isinstance(records, List) and not is_analytics:
            raise ValueError("Error - {}".format(records))

        return records
