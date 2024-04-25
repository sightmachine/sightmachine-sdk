from json.decoder import JSONDecodeError
from time import sleep
import typing as t_
import json
import requests

import numpy as np

from requests.structures import CaseInsensitiveDict
from requests.sessions import Session
from smsdk import config

try:
    import importlib.resources

    RESOURCE_CONFIG = json.loads(
        importlib.resources.read_text(config, "message_config.json")
    )
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources

    RESOURCE_CONFIG = json.loads(
        importlib_resources.read_text(config, "message_config.json")
    )
from smsdk.custom_exception.errors import NotFound

SM_AUTH_HEADER_SECRET_ID = RESOURCE_CONFIG["auth_header-api-secret"]
SM_AUTH_HEADER_SECRET_ID_OLD = RESOURCE_CONFIG["auth_header-api-secret_old"]
SM_AUTH_HEADER_KEY_ID = RESOURCE_CONFIG["auth_header-api-key"]
X_SM_DB_SCHEMA = RESOURCE_CONFIG["x_sm_db_schema"]
X_SM_WORKSPACE_ID = RESOURCE_CONFIG["x_sm_workspace_id"]

import logging

log = logging.getLogger(__name__)


class MaSession:
    def __init__(self) -> None:
        self.requests = requests
        self.session = Session()

    def _get_records(
        self,
        endpoint: str,
        method: str = "get",
        _limit: float = np.Inf,
        _offset: int = 0,
        **url_params: t_.Any,
    ) -> t_.List[t_.Dict[str, t_.Any]]:
        """
        Function to get api call and fetch data from MA APIs
        :param endpoint: complete url endpoint
        :param method: Reqested method. Default = get
        :param enable_pagination: if pagination is enabled then
        the records are fetched with limit offset pagination
        :param limit: Limit the number of records for pagination
        :param offset: pagination offset
        :param url_params: dict of params for API ex filtering, columns etc
        :return: List of records
        """
        if "machine_type" in url_params:
            url_params.pop("machine_type")
        max_page_size = 2000

        records: t_.List[t_.Dict[str, t_.Any]] = []
        while True:
            remaining_limit = _limit - len(records)
            this_loop_limit = int(min(remaining_limit, max_page_size))

            # If we exactly hit our desired number of records -- limit is 0 -- then can stop
            if this_loop_limit <= 0:
                return records

            url_params["_offset"] = _offset
            url_params["_limit"] = this_loop_limit
            print(
                f"==========MA Session{getattr(self.session, method.lower())}{url_params}{endpoint},{method}"
            )
            response = getattr(self.session, method.lower())(
                endpoint, params=url_params
            )

            if response.text:
                if response.status_code == 404:
                    raise NotFound(response.text)
                elif response.status_code not in [200, 201]:
                    raise ValueError("Error - {}".format(response.text))
                try:
                    data = response.json()

                    if "results" in data:
                        data = data["results"]

                except JSONDecodeError as e:
                    # No need to raise an error as this will still continue execution.
                    print(f"No valid JSON returned, but continuing. {e}")
                    continue
            else:
                return []

            records.extend(data)
            if len(data) < this_loop_limit:
                # Cursor exhausted, so just return
                return records
            _offset += this_loop_limit

    def _get_schema(
        self, endpoint: str, method: str = "get", **url_params: t_.Any
    ) -> t_.Any:
        """
        This function can be used to fetch HLO schemas like AIDP
        Function to get api call and fetch data from MA APIs
        :param endpoint: complete url endpoint
        :param method: Reqested method. Default = get
        :param url_params: dict of params for API ex filtering, columns etc
        :return: List of records
        """
        if "machine_type" in url_params:
            url_params.pop("machine_type")

        response = getattr(self.session, method.lower())(endpoint, params=url_params)

        if response.text:
            if response.status_code not in [200, 201]:
                raise ValueError("Error - {}".format(response.text))
            try:
                data = response.json()

                if "objects" in data:
                    data = data["objects"]

                return data
            except JSONDecodeError as e:
                raise JSONDecodeError(
                    "Error decoding JSON response", response.text, e.pos
                )
        else:
            return []

    def _get_records_v1(
        self,
        endpoint: str,
        method: str = "post",
        limit: float = np.Inf,
        offset: float = 0,
        db_mode: str = "sql",
        results_under: str = "results",
        **url_params: t_.Any,
    ) -> t_.List[t_.Dict[str, t_.Any]]:
        """
        Function to get api call and fetch data from MA APIs
        :param endpoint: complete url endpoint
        :param method: Reqested method. Default = get
        :param enable_pagination: if pagination is enabled then
        the records are fetched with limit offset pagination
        :param limit: Limit the number of records for pagination
        :param offset: pagination offset
        :param url_params: dict of params for API ex filtering, columns etc
        :return: List of records
        """
        max_page_size = 50000

        records: t_.List[t_.Dict[str, t_.Any]] = []
        while True:
            try:
                if limit:
                    remaining_limit = limit - len(records)
                    this_loop_limit = min(remaining_limit, max_page_size)

                    # If we exactly hit our desired number of records -- limit is 0 -- then can stop
                    if this_loop_limit == 0:
                        return records
                    url_params["limit"] = this_loop_limit

                if offset or url_params.get("model") == "line":
                    url_params["offset"] = offset
                if db_mode:
                    url_params["db_mode"] = db_mode

                # print(f'Pulling up to {this_loop_limit} records ({remaining_limit} remain)')
                response = None
                try:
                    print(
                        f"==========MA Session{getattr(self.session, method.lower())}{url_params}{endpoint},{method}"
                    )
                    response = getattr(self.session, method.lower())(
                        endpoint, json=url_params
                    )
                except requests.exceptions.ConnectionError:
                    raise ValueError(
                        f"Error connecting to {endpoint}.  Check your tenant name"
                    )

                if response is not None and response.text:
                    if response.status_code not in [200, 201]:
                        raise ValueError(format(response.text))
                    try:
                        data = response.json()
                        if results_under:
                            data = data[results_under]
                        if isinstance(data, dict):
                            data = [data]
                    except JSONDecodeError as e:
                        raise JSONDecodeError(
                            "Error decoding JSON response", response.text, e.pos
                        )
                else:
                    return []

                records.extend(data)
                if limit is None:
                    return records
                if len(data) < this_loop_limit:
                    # Cursor exhausted, so just return
                    return records
                offset += this_loop_limit

            except ValueError as e:
                raise e
            except Exception as e:
                # No need to raise an error as retrying with smaller page size.
                print(f"Error getting data, retrying with smaller page size. {e}")
                # Try throttling down the page size
                max_page_size = int(max_page_size / 2)
                continue

    def _complete_async_task(
        self,
        endpoint: str,
        method: str = "post",
        db_mode: str = "sql",
        **url_params: t_.Any,
    ) -> t_.Any:
        if url_params.get("db_mode") == None:
            url_params["db_mode"] = db_mode
        try:
            response = getattr(self.session, method.lower())(endpoint, json=url_params)
            if response.status_code not in [200, 201]:
                raise ValueError("Error - {}".format(response.text))
            data = response.json()
            task_id = data["response"]["task_id"]
            while True:
                try:
                    response = self.session.get(
                        endpoint + "/" + task_id, json=url_params
                    )
                    sleep(1)
                    if response.status_code not in [200, 201]:
                        raise ValueError("Error - {}".format(response.text))
                    data = response.json()
                    state = data["response"]["state"]
                    if state == "SUCCESS":
                        return data["response"]["meta"]["results"]

                    if state == "FAILURE" or state == "REVOKED":
                        raise ValueError("Error - {}".format(response.text))
                except Exception as e:
                    raise e
        except Exception as e:
            raise e

    def get_json_headers(self) -> CaseInsensitiveDict:
        """
        Headers for json requests
        """
        return CaseInsensitiveDict(
            {
                "Accept-Encoding": "*/*",
                "Content-Type": "application/json",
                "accept": "application/json",
            }
        )

    def get_starttime_endtime_keys(self, **kwargs: t_.Any) -> t_.Tuple[str, str]:
        """
        This function takes kwargs as input and tried to identify starttime and endtime key provided by user and returns
        :param kwargs:
        :return:
        """
        starttime_key = ""
        endtime_key = ""

        times = {i: kwargs[i] for i in kwargs if "time" in i.lower()}

        if times:
            starttime = min(times.values())
            endtime = max(times.values())

            for key in times:
                if times[key] == starttime:
                    starttime_key = key
                elif times[key] == endtime:
                    endtime_key = key
                else:
                    continue

        return starttime_key, endtime_key
