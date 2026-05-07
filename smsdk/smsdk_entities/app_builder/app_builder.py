"""App Builder UDF analysis runner.

Programmatic equivalent of clicking a deployed App Builder app in the
platform UI: starts a `UDFAnalysis` task on `/v1/udf/task/async`, polls
until SUCCESS, and returns the panels list.

Each deployed App Builder page exposes a UDF whose name is
``<deploy_id>_deployed``. The deploy_id is the ``id`` of the deployed-page
record (visible in the platform's URL or via the
`/v1/obj/app_builder_deploy` endpoint). Pickers (date range, dropdowns,
filters, etc.) come from the page's sidebar definition; the caller passes
the values they want.
"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Sequence

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Backport for older Python.
    import importlib_resources as pkg_resources

from smsdk import config
from smsdk.ma_session import MaSession
from smsdk.tool_register import SmsdkEntities, smsdkentities
from smsdk.utils import module_utility


ENDPOINTS = json.loads(pkg_resources.read_text(config, "api_endpoints.json"))


def _build_date_picker(
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    relative_start: Optional[int] = None,
    relative_end: int = -1,
    relative_unit: Optional[str] = None,
    time_zone: str = "Europe/Stockholm",
    time_axis: str = "business_day",
    query_axis: str = "business_day",
) -> Dict[str, Any]:
    """Build the standard ``dateRange`` picker payload.

    Pass either an absolute window (``start_time``/``end_time``, ISO 8601)
    or a relative window (``relative_start``, ``relative_unit`` ∈
    {"day", "week", "month"}).
    """
    if start_time and end_time:
        time_selection: Dict[str, Any] = {
            "time_type": "absolute",
            "start_time": start_time,
            "end_time": end_time,
        }
        mode = "absolute"
        time_type_label = "calendar"
    elif relative_start is not None and relative_unit:
        time_selection = {
            "time_type": "relative",
            "relative_start": relative_start,
            "relative_end": relative_end,
            "relative_unit": relative_unit,
            "time_axis": time_axis,
            "query_axis": query_axis,
            "ctime_tz": None,
        }
        mode = "relative"
        time_type_label = "production"
    else:
        raise ValueError(
            "Provide either start_time+end_time or relative_start+relative_unit."
        )

    return {
        "picker_type": "date",
        "value": {
            "mode": mode,
            "timeType": time_type_label,
            "selectedShortcut": None,
            "selectedTimeZone": time_zone,
            "productionTimeZone": None,
            "currentProductionDay": None,
            "time_selection": time_selection,
            "verboseQuery": False,
        },
    }


@smsdkentities.register("appBuilder")
class AppBuilder(SmsdkEntities, MaSession):
    """SDK entity for App Builder UDF analysis runs."""

    mod_util = module_utility()

    def __init__(self, session, base_url) -> None:
        self.session = session
        self.base_url = base_url

    @mod_util
    def get_utilities(self, *args, **kwargs) -> List[str]:
        """List the registered utility methods on this entity."""
        return [*self.mod_util.all]

    @mod_util
    def get_app_results(
        self,
        deploy_id: str,
        pickers: Optional[Dict[str, Any]] = None,
        date_picker_id: str = "dateRange",
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        relative_start: Optional[int] = None,
        relative_end: int = -1,
        relative_unit: Optional[str] = None,
        time_zone: str = "Europe/Stockholm",
        udf_revision_id: Optional[int] = None,
        *args,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """Run a deployed App Builder app and return its panels.

        :param deploy_id: Deployed-page UUID (the ``id`` field of an
            ``app_builder_deploy`` record). The UDF name is
            ``<deploy_id>_deployed``.
        :param pickers: Optional dict of additional pickers (``choice``,
            ``filter``, etc.) keyed by picker id, in the same shape the
            platform UI sends. The date range is constructed from the
            ``start_time``/``end_time`` or ``relative_*`` arguments and
            merged in under ``date_picker_id``.
        :param date_picker_id: Picker id for the date range. Default
            ``dateRange``. If ``None``, no date range is added (caller
            must include their own in ``pickers``).
        :param start_time: Absolute window start, ISO 8601 string.
        :param end_time: Absolute window end, ISO 8601 string.
        :param relative_start: Relative window start (e.g. ``3``), used
            with ``relative_unit``.
        :param relative_end: Relative window end. Default ``-1``
            (= "ending now").
        :param relative_unit: One of ``"day"``, ``"week"``, ``"month"``.
        :param time_zone: IANA time zone for the date picker.
        :param udf_revision_id: Pin to a specific UDF revision. Default
            ``None`` (= latest deployed).
        :return: List of panel dicts, each with ``viz_type``,
            ``viz_props``, optional ``title``.
        """
        url = "{}{}".format(self.base_url, ENDPOINTS["AppBuilder"]["task"])

        merged_pickers: Dict[str, Any] = dict(pickers or {})
        if date_picker_id is not None:
            merged_pickers[date_picker_id] = _build_date_picker(
                start_time=start_time,
                end_time=end_time,
                relative_start=relative_start,
                relative_end=relative_end,
                relative_unit=relative_unit,
                time_zone=time_zone,
            )

        body = {
            "name": "UDFAnalysis",
            "parameters": {
                "analytics": {
                    "udf_name": f"{deploy_id}_deployed",
                    "udf_revision_id": udf_revision_id,
                    "pickers": merged_pickers,
                },
            },
        }

        result = self._complete_async_task(
            url,
            method="post",
            result_path=("data",),
            send_db_mode=False,
            **body,
        )
        return _extract_panels(result)


def _extract_panels(result: Any) -> List[Dict[str, Any]]:
    """Pull the panels list out of the celery task's wrapped output.

    The UDF endpoint's result shape varies slightly with the platform
    version. We've observed:

    1. ``[{"mime_type": "application/json", "data": {"panels": [...], ...}}]``
       (papermill last-cell output, wrapped by asyncify under ``meta``)
    2. ``{"data": {"panels": [...], ...}}``
    3. ``{"panels": [...]}``

    All three are handled.
    """
    candidate = result
    # Unwrap papermill last-cell list output
    if isinstance(candidate, list) and candidate:
        candidate = candidate[0]
    if isinstance(candidate, dict) and "data" in candidate:
        candidate = candidate["data"]
    if isinstance(candidate, dict):
        return candidate.get("panels", [])
    return []
