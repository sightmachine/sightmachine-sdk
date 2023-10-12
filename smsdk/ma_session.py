from json.decoder import JSONDecodeError
from time import sleep
from typing import List
import json
import requests

import numpy as np

from requests.structures import CaseInsensitiveDict
from requests.sessions import Session

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from smsdk import config

RESOURCE_CONFIG = json.loads(pkg_resources.read_text(config, "message_config.json"))

SM_AUTH_HEADER_SECRET_ID = RESOURCE_CONFIG["auth_header-api-secret"]
SM_AUTH_HEADER_SECRET_ID_OLD = RESOURCE_CONFIG["auth_header-api-secret_old"]
SM_AUTH_HEADER_KEY_ID = RESOURCE_CONFIG["auth_header-api-key"]
X_SM_DB_SCHEMA = RESOURCE_CONFIG["x_sm_db_schema"]
X_SM_WORKSPACE_ID = RESOURCE_CONFIG["x_sm_workspace_id"]

import logging

log = logging.getLogger(__name__)


class MaSession:
    def __init__(self):
        self.requests = requests
        self.session = Session()

    def _get_records(
        self, endpoint, method="get", _limit=np.Inf, _offset=0, **url_params
    ):
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

        records: List = []
        while True:
            try:
                remaining_limit = _limit - len(records)
                this_loop_limit = min(remaining_limit, max_page_size)

                # If we exactly hit our desired number of records -- limit is 0 -- then can stop
                if this_loop_limit <= 0:
                    return records

                url_params["_offset"] = _offset
                url_params["_limit"] = this_loop_limit

                # print(f'Pulling up to {this_loop_limit} records ({remaining_limit} remain)')
                response = getattr(self.session, method.lower())(
                    endpoint, params=url_params
                )
                # print(f"response text -- {response.text}")

                if response.text:
                    if response.status_code not in [200, 201]:
                        raise ValueError("Error - {}".format(response.text))
                    try:
                        data = response.json()

                        if "results" in data:
                            data = data["results"]

                    except JSONDecodeError as e:
                        print(f"No valid JSON returned, but continuing. {e}")
                        continue
                else:
                    return []

                records.extend(data)
                # print(f'sizes {len(data)} vs {this_loop_limit}')
                if len(data) < this_loop_limit:
                    # Cursor exhausted, so just return
                    return records
                _offset += this_loop_limit

            except Exception as e:
                print(f"Error getting data, but continuing. {e}")
                continue

    def _get_schema(self, endpoint, method="get", **url_params):
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
                print(f"No valid JSON returned {e}")
                return []
        else:
            return []

    def _get_records_v1(
        self,
        endpoint,
        method="post",
        limit=np.Inf,
        offset=0,
        db_mode="sql",
        results_under="results",
        **url_params,
    ):
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

        records: List = []
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

                response = getattr(self.session, method.lower())(
                    endpoint, json=url_params
                )

                if response.text:
                    if response.status_code not in [200, 201]:
                        raise ValueError(format(response.text))
                    try:
                        data = response.json()
                        if results_under:
                            data = data[results_under]
                        if isinstance(data, dict):
                            data = [data]
                    except JSONDecodeError as e:
                        print(f"No valid JSON returned {e}")
                        return []
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
                print(f"Error getting data, retrying with smaller page size. {e}")
                # Try throttling down the page size
                max_page_size = int(max_page_size / 2)
                continue

    def _complete_async_task(
        self, endpoint, method="post", db_mode="sql", **url_params
    ):
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
                except:
                    return response.text
        except:
            return response.text

    def get_json_headers(self):
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

    def get_starttime_endtime_keys(self, **kwargs):
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
