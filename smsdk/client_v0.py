#!/usr/bin/env python
# coding: utf-8
""" Sight Machine SDK Client """
from __future__ import unicode_literals, absolute_import

from copy import deepcopy

import numpy as np
import pandas as pd
import pathos
import typing as t_

try:
    # for newer pandas versions >1.X
    from pandas import json_normalize
except ImportError:
    from pandas.io.json import json_normalize

from smsdk.utils import get_url
from smsdk.Auth.auth import Authenticator
from smsdk.tool_register import smsdkentities

from datetime import datetime
import logging
import functools
from urllib.parse import urlparse

log = logging.getLogger(__name__)


def time_string_to_epoch(time_string):
    try:
        dt = pd.to_datetime(time_string)
        time_epoch = (
            dt - pd.to_datetime("1970-01-01")
        ).total_seconds() * 1000  # SM timestamps in ms
    except ValueError as e:
        log.error(f"Unable to parse time string {time_string}: {e}")
        return 0
    except Exception as e:
        log.error(f"Bad date specified: {time_string}")
        return 0

    return time_epoch


def dict_to_df(data, normalize=True):
    if normalize:
        # special case to handle the 'stats' block
        if data and "stats" in data[0]:
            if isinstance(data[0]["stats"], dict):
                # part stats are dict
                df = json_normalize(data)
            else:
                # machine type stats are list
                cols = [*data[0]]
                cols.remove("stats")
                if "part_types" in cols:
                    cols.remove("part_types")
                df = json_normalize(data, "stats", cols, record_prefix="stats.")
        else:
            try:
                df = json_normalize(data)
            except:
                # From cases like _distinct which don't have a "normal" return format
                return pd.DataFrame({"values": data})
    else:
        df = pd.DataFrame(data)

    if len(df) > 0:
        if "_id" in df.columns:
            df.set_index("_id", inplace=True)

        if "id" in df.columns:
            df.set_index("id", inplace=True)

    return df


def convert_to_valid_url(
    input_url: str,
    default_domain: str = "sightmachine.io",
    default_protocol: str = "https",
):
    port = ""
    path = ""

    # Check if the input URL has a protocol specified
    if "://" in input_url:
        protocol, rest_url = input_url.split("://", 1)
    else:
        protocol = default_protocol
        rest_url = input_url

    if not protocol:
        protocol = default_protocol

    # Split the remaining URL to check if domain is specified
    parts = rest_url.split("/", 1)

    if len(parts) == 1:
        domain = parts[0]
        path = ""
    else:
        domain, path = parts

    # Check if the domain has a port specified
    splits = domain.split(":", 1)

    if len(splits) == 2:
        domain, port = splits

    # Check if the domain has a TLD or not
    if "." not in domain:
        domain = f"{domain}.{default_domain}"

    # Check if domain endswith default domain
    if not domain.endswith(default_domain):
        domain = f"{domain}.{default_domain}"

    # Construct the valid URL
    valid_url = f"{protocol}://{domain}"

    if port:
        valid_url = f"{valid_url}:{port}"
        # log.warning(f"Ignored the user specified port.")

    if path:
        # valid_url = f"{valid_url}/{path}"
        log.warning(f"Ignored the user specified path.")

    return valid_url


# We don't have a downtime schema, so hard code one
downmap = {
    "machine__source": "Machine",
    "starttime": "Start Time",
    "endtime": "End Time",
    "total": "Duration",
    "shift": "Shift",
    "reason": "Downtime Reason",
    "category": "Downtime Category",
    "downtime_type": "Downtime Type",
}

downmapinv = {
    "Machine": "machine__source",
    "Start Time": "starttime",
    "End Time": "endtime",
    "Duration": "total",
    "Shift": "shift",
    "Downtime Reason": "reason",
    "Downtime Category": "category",
    "Downtime Type": "downtime_type",
}


class ClientV0(object):
    """Connection point to the Sight Machine platform to retrieve data"""

    session = None
    tenant = None
    config = {}

    def __init__(
        self, tenant: str, site_domain: str = "sightmachine.io", protocol: str = "https"
    ):
        """
        Initialize the client.

        :param tenant: The tenant within Sight Machine to access.
        :type tenant: :class:`string`
        :param site_domain:
            The site domain to connect to. Necessary to change if deploying in
            a non-standard environment.
        :type site_domain: :class:`string`
        """

        port = None
        if tenant:
            # Convert the input tenant into a valid url
            url = convert_to_valid_url(
                tenant, default_domain=site_domain, default_protocol=protocol
            )

            # Parse the input string
            parsed_uri = urlparse(url)

            tenant = parsed_uri.netloc.split(".", 1)[0]
            protocol = parsed_uri.scheme
            site_domain = parsed_uri.netloc.split(":")[0].replace(f"{tenant}.", "")

            # Extract port
            port = parsed_uri.port

        self.tenant = tenant
        self.config = {"protocol": protocol, "site.domain": site_domain, "port": port}

        # Setup Authenticator
        self.auth = Authenticator(self)
        self.session = self.auth.session

    def login(self, method: str, **kwargs: t_.Any) -> bool:
        """
        Authenticate with the configured tenant and user credentials.

        cli.login('basic', email='user@domain.com', password='password')

        or

        cli.login('apikey', key_id='api_key_string', secret_id='api_secret_string')

        :param method: The authentication method: apikey or basic
        :type method: :class:`string`
        :param kwargs:
            By method:
                * apikey - key_id, secret_id
                * basic - email, password
        """
        return self.auth.login(method, **kwargs)

    def logout(self, **kwargs):
        """
        Unauthenticate from the configured tenant
        """
        return self.auth.logout(**kwargs)

    def list_entities(self):
        """
        Return the list of registered entites.  Primarily used if making direct get_data calls.  Generally for internal use only.
        """
        return [e.name for e in smsdkentities.list()]

    def fix_only(self, kwargs):
        if not "_only" in kwargs:
            return [kwargs]

        only_size = len(str(kwargs["_only"]))
        num_chunks = np.ceil(only_size / 1500)
        # assume string size corresponds roughtly to number of entries
        chunk_sz = int(np.ceil(len(kwargs["_only"]) / num_chunks))

        chunks = []
        for x in range(0, len(kwargs["_only"]), chunk_sz):
            kw = kwargs.copy()
            kw["_only"] = str(kw["_only"][x : x + chunk_sz])
            chunks.append(kw)

        return chunks

    def validate_input(func):
        """This decorator can be used to validate input schema with some conditions,
        or can implement jsonschema validator in later versions if required"""

        @functools.wraps(func)
        def validate(*args, **kwargs):
            exceptional_keys = ["_only"]
            for key in kwargs:
                if key in exceptional_keys:
                    continue
                if isinstance(kwargs[key], list):
                    if not (key.endswith("__in") or key.endswith("__nin")):
                        msg = f"Key <{key}> should have '__in' or '__nin' in it if datatype is list"
                        raise ValueError(msg)
            return func(*args, **kwargs)

        return validate

    def get_data(self, ename, util_name, normalize=True, *args, **kwargs):
        """
        Main data fetching function for all the entities.  Note this is the general data fetch function.  You probably want to use the model-specific functions such as get_cycles().
        :param ename: Name of the entities
        :param util_name: Name of the utility function
        :param normalize: Flatten nested data structures
        :return: pandas dataframe
        """
        base_url = get_url(
            self.config["protocol"],
            self.tenant,
            self.config["site.domain"],
            self.config["port"],
        )

        df = pd.DataFrame()
        # load the entity class and initialize it
        cls = smsdkentities.get(ename)(self.session, base_url)

        # In the current API, filter by start/endtime + anything else is broken
        # But you can properly filter by epoch + other, so automatically convert those
        for kw in [
            "endtime",
            "endtime__gt",
            "endtime__lt",
            "endtime__gte",
            "endtime__lte",
            "starttime",
            "starttime__gt",
            "starttime__lt" "starttime__gte",
            "starttime__lte",
        ]:
            if kw in kwargs:
                original_time = kwargs.pop(kw)
                epoch_time = time_string_to_epoch(original_time)
                new_kw = kw.replace("endtime", "endtime_epoch").replace(
                    "starttime", "starttime_epoch"
                )
                kwargs[new_kw] = epoch_time

        # The current API is inconsistent where most paramters use the MongoEngine-like __ notation for ., but _only requires .
        # So let the user enter '__', but convert those to '.' for API compatibility
        if "_only" in kwargs:
            new_cols = []
            for colname in kwargs.pop("_only"):
                new_cols.append(colname.replace("__", "."))
            kwargs["_only"] = new_cols

        # Fix format for __in commands
        for key, val in kwargs.items():
            if "__in" in key:
                kwargs[key] = str(val)

        # check if requested util_name belong the list of
        # registerd utilites
        if util_name in getattr(cls, "get_utilities")(*args, **kwargs):
            # call the utility function
            # all the dict params are passed as kwargs
            # dict params strictly follow {'key':'value'} format

            sub_kwargs = self.fix_only(kwargs)

            if len(sub_kwargs) == 1:
                data = dict_to_df(
                    getattr(cls, util_name)(*args, **sub_kwargs[0]), normalize
                )
            else:
                data = dict_to_df(
                    getattr(cls, util_name)(*args, **sub_kwargs[0]), normalize
                )

                for sub in sub_kwargs[1:]:
                    sub_data = dict_to_df(
                        getattr(cls, util_name)(*args, **sub), normalize
                    )
                    data = data.join(sub_data, rsuffix="__joined")

                    joined_cols = [col for col in data.columns if "__joined" in col]
                    data.drop(joined_cols, axis=1)

            # To keep consistent, rename columns back from '.' to '__'
            data.columns = [name.replace(".", "__") for name in data.columns]

        else:
            # raise error if requested for unregistered utility
            raise ValueError("Error - {}".format("Not a registered utility"))

        if "endtime" in data.columns:
            data["endtime"] = pd.to_datetime(data["endtime"])
        if "starttime" in data.columns:
            data["starttime"] = pd.to_datetime(data["starttime"])

        return data

    """
    HLO Decorators, that can be used by both V0 & V1 if logic will be similar before processing  
    """

    def cycle_decorator(func):
        @functools.wraps(func)
        def inner(
            self,
            normalize=True,
            clean_strings_in=True,
            clean_strings_out=True,
            *args,
            **kwargs,
        ):
            # When processing in batch
            if args and (not kwargs):
                kwargs = args[0]

            machine = kwargs.get("machine__source", kwargs.get("Machine"))
            if not machine:
                # Possible that it is a machine__in.  If so, base on first machine
                machine = kwargs.get("machine__source__in", kwargs.get("Machine__in"))
            kwargs["machine__source"] = machine
            if isinstance(machine, str):
                machine_type, schema = self.get_machine_schema(
                    machine, return_mtype=True
                )
            else:  # it is a list of machines, work with first name in list
                machine_type, schema = self.get_machine_schema(
                    machine[0], return_mtype=True
                )

            if "_limit" not in kwargs:
                print("_limit not specified. Maximum of 5000 rows will be returned.")
                kwargs["_limit"] = 5000
            elif kwargs["_limit"] > 5000:
                print(
                    "Warning: _limit over 5000 specified. Setting excessively large limits may lead to timeouts."
                )

            if not "_only" in kwargs:
                print("_only not specified.  Selecting first 50 fields.")
                only_names = schema["name"].tolist()[:50]
                kwargs["_only"] = only_names
            else:
                if all(
                    i not in {"End Time", "endtime", "Cycle End Time"}
                    for i in kwargs["_only"]
                ):
                    print("Adding End Time to _only")
                    kwargs["_only"].insert(0, "End Time")

                if all(
                    i not in {"Machine", "machine__source"} for i in kwargs["_only"]
                ):
                    print("Adding Machine to _only")
                    kwargs["_only"].insert(0, "Machine")

            if kwargs["_only"] == "*":
                kwargs.pop("_only")

            if "_only" in kwargs:
                available_names = set(
                    schema["name"].to_list()
                    + schema["display"].to_list()
                    + [
                        "record_time",
                        "endtime",
                        "total",
                        "machine__source",
                        "starttime",
                        "output",
                        "shift",
                    ]
                    + [
                        "Cycle Time (Gross)",
                        "End Time",
                        "Cycle Time (Net)",
                        "Machine",
                        "Start Time",
                        "Output",
                        "Shift",
                    ]
                )
                used_names = set(kwargs["_only"])
                different_names = used_names.difference(available_names)

                if len(different_names) > 0:
                    print(
                        f'Dropping invalid column names: {", ".join(different_names)}.'
                    )
                    kwargs["_only"] = used_names.intersection(available_names)

            if clean_strings_in:
                kwargs = self.clean_query_machine_titles(kwargs)
                kwargs = self.clean_query_machine_names(kwargs)

            kwargs.update({"machine_type": machine_type})
            df = func(
                self, normalize, clean_strings_in, clean_strings_out, *args, **kwargs
            )

            if len(df) > 0 and clean_strings_out:
                df = self.clean_df_machine_titles(df)
                df = self.clean_df_machine_names(df)
            return df

        return inner

    def downtime_decorator(func):
        @functools.wraps(func)
        def inner(
            self,
            normalize=True,
            clean_strings_in=True,
            clean_strings_out=True,
            *args,
            **kwargs,
        ):
            # When processing in batch
            if args and (not kwargs):
                kwargs = args[0]

            if "_limit" not in kwargs:
                print("_limit not specified. Maximum of 5000 rows will be returned.")
                kwargs["_limit"] = 5000
            elif kwargs["_limit"] > 5000:
                print(
                    "Warning: _limit over 5000 specified. Setting excessively large limits may lead to timeouts."
                )

            if not "_only" in kwargs:
                kwargs["_only"] = downmap.keys()

            machine = kwargs.get("machine__source", kwargs.get("Machine"))
            if not machine:
                # Possible that it is a machine__in.  If so, base on first machine
                machine = kwargs.get("machine__source__in", kwargs.get("Machine__in"))
            kwargs["machine__source"] = machine

            machine_type, schema = self.get_machine_schema(machine, return_mtype=True)
            # schema = schema['name'].tolist()[:50]
            if clean_strings_in:
                kwargs = self.clean_query_downtime_titles(kwargs)
                kwargs = self.clean_query_machine_names(kwargs)

            kwargs.update({"machine_type": machine_type})
            # df = self.get_data('downtime', 'get_downtime', normalize, *args, **kwargs)
            df = func(
                self,
                normalize=True,
                clean_strings_in=True,
                clean_strings_out=True,
                *args,
                **kwargs,
            )

            # if clean_strings_out:
            if len(df) > 0 and clean_strings_out:
                df = self.clean_df_downtime_titles(df)
                df = self.clean_df_machine_names(df)

            return df

        return inner

    def part_decorator(func):
        # def inner(self, normalize=True, clean_strings_in=True, clean_strings_out=True, datatab_api=False, *args, **kwargs):
        @functools.wraps(func)
        def inner(
            self,
            normalize=True,
            clean_strings_in=True,
            clean_strings_out=True,
            datatab_api=False,
            *args,
            **kwargs,
        ):
            """Accessing default value of datatab_api because for V0 it'll be False and for V1 it'll be true"""
            datatab_api = func.__defaults__[3]

            # When processing in batch
            if args and (not kwargs):
                kwargs = args[0]

            part = kwargs.get("type__part_type", kwargs.get("Part"))
            if not part:
                part = kwargs.get("type__part_type__in", kwargs.get("Part__in"))
                part = part[0]

            kwargs["type__part_type"] = part
            part_schema = self.get_part_schema(part)

            if "_limit" not in kwargs:
                print("_limit not specified. Maximum of 5000 rows will be returned.")
                kwargs["_limit"] = 5000
            elif kwargs["_limit"] > 5000:
                print(
                    "Warning: _limit over 5000 specified. Setting excessively large limits may lead to timeouts."
                )

            if "_only" not in kwargs:
                print("_only not specified.  Selecting first 50 fields.")

                cols = part_schema["name"].tolist()[:50]

                toplevel = [
                    "type__part_type",
                    "serial",
                    "starttime",
                    "endtime",
                    "production_date_start",
                    "production_date_end",
                    "metadata__nettime",
                    "state",
                ]

                kwargs["_only"] = toplevel + cols

            if clean_strings_in:
                kwargs = self.clean_query_part_titles(kwargs)
                kwargs = self.clean_query_part_names(kwargs)

            if "type__part_type" not in kwargs["_only"]:
                kwargs["_only"].insert(0, "type__part_type")

            # df = self.get_data('downtime', 'get_downtime', normalize, *args, **kwargs)
            df = func(
                self, normalize, clean_strings_in, clean_strings_out, *args, **kwargs
            )

            # if clean_strings_out:
            if len(df) > 0 and clean_strings_out:
                df = self.clean_df_part_names(df)
                df = self.clean_df_part_titles(df, part_schema, datatab_api)

            return df

        return inner

    def get_machine_schema_decorator(func):
        @functools.wraps(func)
        def inner(
            self,
            machine_source,
            types=[],
            show_hidden=False,
            return_mtype=False,
            **kwargs,
        ):
            try:
                machine_type = self.get_machines(source=machine_source)["source_type"][
                    0
                ]
            except KeyError:
                try:
                    machine_type = self.get_machines(source=f"'{machine_source}'")[
                        "source_type"
                    ][0]
                except KeyError:
                    try:
                        # Possible that this was done on a clean string
                        machine_type = self.get_machines(source_clean=machine_source)[
                            "source_type"
                        ][0]
                    except KeyError:
                        log.error(f"Unable to find machine type for {machine_source}")
                        return
            try:
                stats = self.get_machine_types(
                    normalize=False, _limit=1, source_type=machine_type
                )["stats"][0]
            except KeyError:
                # explicitly embed string to machine type names esp JCP
                machine_type = f"'{machine_type}'"
                stats = self.get_machine_types(
                    normalize=False, _limit=1, source_type=machine_type
                )["stats"][0]
            except Exception as ex:
                print(f"Exception in getting machine type stats {ex}")
            kwargs["stats"] = stats

            fields = func(
                self, machine_source, types, show_hidden, return_mtype, **kwargs
            )

            if return_mtype:
                return machine_type, pd.DataFrame(fields)

            return pd.DataFrame(fields)

        return inner

    # Some shortcut functions
    @validate_input
    @cycle_decorator
    def get_cycles(
        self,
        normalize=True,
        clean_strings_in=True,
        clean_strings_out=True,
        *args,
        **kwargs,
    ):
        """
        Retrieve cycle/machine data.

        :param normalize: Flatten nested data structures
        :type normalize: bool
        :param clean_strings_in: When using query parameters, converts the UI-based display names into the Sight Machine internal database names.
        :type clean_strings_in: bool
        :param clean_strings_out: For the returned data frame, convert the Sight Machine internal database names into the UI-based display names.
        :type clean_strings_out: bool
        :return: pandas dataframe
        """

        df = self.get_data("cycle", "get_cycles", normalize, *args, **kwargs)

        return df

    @validate_input
    @downtime_decorator
    def get_downtimes(
        self,
        normalize=True,
        clean_strings_in=True,
        clean_strings_out=True,
        *args,
        **kwargs,
    ):
        """
        Retrieve Downtime data.

        :param normalize: Flatten nested data structures
        :type normalize: bool
        :param clean_strings_in: When using query parameters, converts the UI-based display names into the Sight Machine internal database names.
        :type clean_strings_in: bool
        :param clean_strings_out: For the returned data frame, convert the Sight Machine internal database names into the UI-based display names.
        :type clean_strings_out: bool
        :return: pandas dataframe
        """

        df = self.get_data("downtime", "get_downtime", normalize, *args, **kwargs)

        return df

    def get_downtime_reasons(self, machine=None):
        query = {"_distinct": "metadata.reason"}

        if machine:
            query["Machine"] = machine

        reason_df = self.get_downtimes(clean_strings_out=False, **query)

        if "values" in reason_df.keys():
            return reason_df["values"].to_list()
        else:
            return []

    @validate_input
    @part_decorator
    def get_parts(
        self,
        normalize=True,
        clean_strings_in=True,
        clean_strings_out=True,
        *args,
        **kwargs,
    ):
        """
        Retrieve Downtime data.

        :param normalize: Flatten nested data structures
        :type normalize: bool
        :param clean_strings_in: When using query parameters, converts the UI-based display names into the Sight Machine internal database names.
        :type clean_strings_in: bool
        :param clean_strings_out: For the returned data frame, convert the Sight Machine internal database names into the UI-based display names.
        :type clean_strings_out: bool
        :return: pandas dataframe
        """
        # kwargs, part_schema = self.clean_query_part_titles(kwargs)
        data = self.get_data("parts", "get_parts", normalize, *args, **kwargs)

        # data = self.clean_df_part_titles(data, part_schema)

        # part_schema = self.get_data('parts','get_part_schema', False, *args, **kwargs)
        # return part_schema
        return data

    def get_downtimes_with_cycles(
        self,
        normalize=True,
        clean_strings_in=True,
        clean_strings_out=True,
        *args,
        **kwargs,
    ):
        """
        Merges cycle and downtime data where each downtime record also has its preceeding cycle stats.  Parameters are
        identical to get_downtimes(), but the returned data structure will also have corresponding cycle data from immediately before each downtime.

        Note this function takes time as it is handling many queries to assemble the resulting data frame.

        :param normalize: Flatten nested data structures
        :type normalize: bool
        :param clean_strings_in: When using query parameters, converts the UI-based display names into the Sight Machine internal database names.
        :type clean_strings_in: bool
        :param clean_strings_out: For the returned data frame, convert the Sight Machine internal database names into the UI-based display names.
        :type clean_strings_out: bool
        :return: pandas dataframe
        """

        df = self.get_downtimes(
            normalize=normalize,
            clean_strings_in=clean_strings_in,
            clean_strings_out=clean_strings_out,
            **kwargs,
        )

        # Get the cycle before each downtime record
        cycs = []
        for row in df.iterrows():
            query = {
                "machine__source": row[1].get("Machine", row[1].get("machine__source")),
                "starttime__lte": row[1].get("Start Time", row[1].get("starttime")),
                "_limit": 1,
                "_order_by": "-starttime",
            }
            cycs.append(
                self.get_cycles(
                    clean_strings_in=clean_strings_in,
                    clean_strings_out=clean_strings_out,
                    **query,
                )
            )
        df_cyc = pd.concat(cycs)

        # Just joining by row, so reset all the indexes to just the row number and get rid of the mongo object id
        df = df.reset_index()
        df = df.drop("id", axis=1, errors="ignore")
        df_cyc = df_cyc.reset_index()
        if clean_strings_out:
            df_cyc = df_cyc.drop(
                ["Machine", "id", "Shift"], axis=1, errors="ignore"
            )  # Also get rid of fields that are duplicate on both downtime and cycle
            df_cyc = df_cyc.rename(
                {"Start Time": "Cycle Start Time", "End Time": "Cycle End Time"}, axis=1
            )  # Retitle times so clear these are from the cycle
        else:
            df_cyc = df_cyc.drop(
                ["machine__source", "id", "shift"], axis=1, errors="ignore"
            )  # Also get rid of fields that are duplicate on both downtime and cycle
            df_cyc = df_cyc.rename(
                {"starttime": "cycle_starttime", "End Time": "cycle_endtime"}, axis=1
            )  # Retitle times so clear these are from the cycle

        merged = df.merge(df_cyc, left_index=True, right_index=True)

        return merged

    def get_factories(self, normalize=True, *args, **kwargs):
        """
        Get list of factories and associated metadata.  Note this includes extensive internal metadata.

        :param normalize: Flatten nested data structures
        :type normalize: bool
        :return: pandas dataframe
        """
        return self.get_data("factory", "get_factories", normalize, *args, **kwargs)

    def get_machines(self, normalize=True, *args, **kwargs):
        """
        Get list of machines and associated metadata.  Note this includes extensive internal metadata.  If you only want to get a list of machine names
        then see also get_machine_names().

        :param normalize: Flatten nested data structures
        :type normalize: bool
        :return: pandas dataframe
        """
        return self.get_data("machine", "get_machines", normalize, *args, **kwargs)

    def get_machine_names(self, source_type=None, clean_strings_out=True):
        """
        Get a list of machine names.  This is a simplified version of get_machines().

        :param source_type: filter the list to only the specified source_type
        :type source_type: str
        :param clean_strings_out: If true, return the list using the UI-based display names.  If false, the list contains the Sight Machine internal machine names.
        :return: list
        """

        query_params = {
            "_only": ["source", "source_clean", "source_type"],
            "_order_by": "source_clean",
        }

        if source_type:
            # Double check the type
            mt = self.get_machine_types(source_type=source_type)
            # If it was found, then no action to take, otherwise try looking up from clean string
            if not len(mt):
                mt = self.get_machine_types(source_type_clean=source_type)
                if len(mt):
                    source_type = mt["source_type"].iloc[0]
                else:
                    log.error("Machine Type not found")
                    return []

            query_params["source_type"] = source_type

        machines = self.get_data(
            "machine", "get_machines", normalize=True, **query_params
        )

        if clean_strings_out:
            return machines["source_clean"].to_list()
        else:
            return machines["source"].to_list()

    @get_machine_schema_decorator
    def get_machine_schema(
        self, machine_source, types=[], return_mtype=False, **kwargs
    ):
        stats = kwargs.get("stats", [])
        fields = []
        for stat in stats:
            if not stat.get("display", {}).get("ui_hidden", False):
                if len(types) == 0 or stat["analytics"]["columns"][0]["type"] in types:
                    try:
                        fields.append(
                            {
                                "name": f'stats__{stat["title"]}__val',
                                # 'name': stat['analytics']['columns'][0]['name'],
                                "display": stat["display"]["title_prefix"],
                                "type": stat["analytics"]["columns"][0]["type"],
                            }
                        )
                    except:
                        log.warning(
                            f"Unknow stat schema identified :: machine_type {machine_source} - "
                            f"title_prefix :: {stat.get('display', {}).get('title_prefix', '')}"
                        )
        return fields

    def get_machine_timezone(self, machine_source):
        """
        Get the timezone associated with a machine.

        :param machine_source
        :type machine_source: str
        :return: pandas dataframe
        """

        mach = self.get_machines(**{"source": machine_source})
        if len(mach) == 0:
            mach = self.get_machines(**{"source_clean": machine_source})
            if len(mach) == 0:
                raise Exception("Machine not found")

        partner = mach.iloc[0]["factory_partner"]
        location = mach.iloc[0]["factory_location"]

        fact = self.get_factories(factory_partner=partner, factory_location=location)
        timezone = fact.iloc[0]["metadata__timezone"]

        return timezone

    def get_machine_types(self, normalize=True, *args, **kwargs):
        """
        Get list of machine types and associated metadata.  Note this includes extensive internal metadata.  If you only want to get a list of machine type names
        then see also get_machine_type_names().

        :param normalize: Flatten nested data structures
        :type normalize: bool
        :return: pandas dataframe
        """

        return self.get_data(
            "machine_type", "get_machine_types", normalize, *args, **kwargs
        )

    def get_machine_type_names(self, clean_strings_out=True):
        """
        Get a list of machine type names.  This is a simplified version of get_machine_types().

        :param clean_strings_out: If true, return the list using the UI-based display names.  If false, the list contains the Sight Machine internal machine types.
        :return: list
        """
        query_params = {
            "_only": ["source_type", "source_type_clean"],
            "_order_by": "source_type_clean",
        }
        machine_types = self.get_data(
            "machine_type", "get_machine_types", normalize=True, **query_params
        )
        if clean_strings_out:
            return machine_types["source_type_clean"].to_list()
        else:
            return machine_types["source_type"].to_list()

    def clean_df_part_names(self, table):
        part_names = self.get_data("parts", "get_all_parts", normalize=False)[
            ["part_type", "part_type_clean"]
        ].to_dict(orient="records")
        part_map = {ptn["part_type"]: ptn["part_type_clean"] for ptn in part_names}

        table["type__part_type"] = table["type__part_type"].apply(
            lambda pt: part_map.get(pt, pt)
        )

        return table

    def clean_df_part_titles(self, table, part_schema, datatab_api=False):
        """
        Convert the dataframe column names on Cycle data from the Sight Machine internal name to the user-friendly names.
        If machine is not provided, assumes that there is a column named machine__source to lookup name from first row.
        Function is used to clean up returned results from get_cycle() query requests.

        :param table: A pandas data table with cycle or part data
        :type table: class:`DataFrame`
        :param machine: Optional machine type for looking up the raw -> display column definitions
        :type machine: class:`string`
        :return: pandas dataframe
        """

        part_schema = part_schema[["display", "name"]].to_dict("records")

        colmap = {i["name"]: i["display"] for i in part_schema}
        toplevelinv = {
            "endtime": "Cycle End Time",
            "starttime": "Cycle Start Time",
            "type__part_type": "Part",
            "metadata__nettime": "Total Cycle Time (Net)",
            "serial": "Serial",
            "production_date_start": "Production Day Start",
            "production_date_end": "Production Day End",
            "state": "State (Pass / Fail)",
        }
        colmap.update(toplevelinv)

        table = table.rename(colmap, axis=1)
        return table

    def get_part_schema(self, part_type, types=[], **kwargs):
        fields = []

        all_parts = self.get_data("parts", "get_all_parts", normalize=False)
        pt = part_type or kwargs.get("Part Type", kwargs.get("type__part_type", None))
        if not pt:
            print("No Part Type Specified")

        stats = all_parts.loc[
            (all_parts.part_type == pt) | (all_parts.part_type_clean == pt), "stats"
        ][0]

        for machine in stats.keys():
            m_stats = stats[machine]

            for m_stat in m_stats.values():
                if not m_stat.get("display", {}).get("ui_hidden", False):
                    if (
                        len(types) == 0
                        or m_stat["analytics"]["columns"][0]["type"] in types
                    ):
                        fields.append(
                            {  #'name': f'stats__{m_stat["title"]}__val',
                                "name": m_stat["analytics"]["columns"][0]["name"],
                                "display": m_stat["display"]["title_prefix"],
                                "type": m_stat["analytics"]["columns"][0]["type"],
                            }
                        )
        part_schema = pd.DataFrame(fields)

        return part_schema

    def clean_query_part_names(self, query):
        part_names = self.get_data("parts", "get_all_parts", normalize=False)[
            ["part_type", "part_type_clean"]
        ].to_dict(orient="records")
        part_map = {ptn["part_type_clean"]: ptn["part_type"] for ptn in part_names}
        pt = query["type__part_type"]

        query["type__part_type"] = part_map.get(pt, pt)

        return query

    def clean_query_part_titles(self, query):
        """
        Given a query for cycles that uses UI friendly tag/field names, convert the machines back into the internal Sight Machine names

        :param query: Dict kwargs passed as part of a query to the API

        :return: dict
        """
        query = query.copy()

        # First need to find the machine name
        part = query.get("type__part_type", query.get("Part"))
        if not part:
            # Possible that it is a machine__in.  If so, base on first machine
            part = query.get("type__part_type__in", query.get("Part__in"))
            part = part[0]

        # schema = self.get_machine_schema(part)
        # schema = self.get_data('parts','get_part_schema', False, **query)
        schema = self.get_part_schema(part)
        part_schema = schema.to_dict("records")

        colmap = {i["display"]: i["name"] for i in part_schema}

        toplevel = {
            "End Time": "endtime",
            "Start Time": "starttime",
            "Part Type": "type__part_type",
            "Part": "type__part_type",
            "Serial": "serial",
            "Cycle Time (Net)": "total",
            "Cycle Time (Gross)": "record_time",
            "Shift": "shift",
            "Output": "output",
        }
        colmap.update(toplevel)

        translated_query = {}
        for key, val in query.items():
            # Special handling for _order_by since the stat titles are in a list
            if key == "_order_by":
                prefix = ""
                if val.startswith("-"):
                    val = val[1:]
                    prefix = "-"
                val = colmap.get(val, val)

                if val == "endtime":
                    val = "endtime_epoch"
                if val == "starttime":
                    val = "starttime_epoch"

                # For performance, currently only support order by time, machine
                if not val in ["endtime_epoch", "starttime_epoch", "machine__source"]:
                    log.warn(
                        "Only ordering by start time, end time, and machine source currently supported."
                    )
                    continue

                val = f"{prefix}{val}"

            # Special handling for _only
            elif key == "_only":
                # To simplify the logic, always treat as a list of _only items
                if isinstance(val, str):
                    val = [val]

                val = [colmap.get(col, col) for col in val]

            # for all other params
            else:
                func = ""
                if "__" in key:
                    parts = key.split("__")
                    key = "__".join(parts[:-1])
                    func = parts[-1]

                    if not func in [
                        "in",
                        "nin",
                        "gt",
                        "lt",
                        "gte",
                        "lte",
                        "exists",
                        "ne",
                        "eq",
                    ]:
                        # This isn't actually a function.  Probably another nested item like machine__source
                        key = f"{key}__{func}"
                        func = ""

                key = colmap.get(key, key)
                if key in colmap and key not in toplevel:
                    key = f"stats__{key}__val"

                if func:
                    key = f"{key}__{func}"

            translated_query[key] = val

        return translated_query

    def clean_df_machine_titles(self, table, machine=None):
        """
        Convert the dataframe column names on Cycle data from the Sight Machine internal name to the user-friendly names.
        If machine is not provided, assumes that there is a column named machine__source to lookup name from first row.
        Function is used to clean up returned results from get_cycle() query requests.

        :param table: A pandas data table with cycle or part data
        :type table: class:`DataFrame`
        :param machine: Optional machine type for looking up the raw -> display column definitions
        :type machine: class:`string`
        :return: pandas dataframe
        """

        if not machine:
            try:
                machine = table.loc[:, "machine__source"].iloc[0]
            except KeyError as e:
                try:
                    # Maybe it was already cleaned
                    machine = table.loc[:, "Machine"].iloc[0]
                except KeyError as e:
                    log.error(f"Unable to lookup source type for schema: {e}")
                    return table

        # Handle EF type machine names
        # Commenting these out because we already are getting machine_names as string even if they are in numerics.
        # if len(machine) <= 6 and machine[:3].isnumeric():
        #     machine = f"'{machine}'"

        # Handle EF type machine names
        # if len(machine) == 5 and machine[:3].isnumeric():
        #     machine = f"'{machine}'"

        schema = self.get_machine_schema(machine)

        colmap = {row[1]["name"]: row[1]["display"] for row in schema.iterrows()}
        toplevelinv = {
            "endtime": "End Time",
            "starttime": "Start Time",
            "machine__source": "Machine",
            "total": "Cycle Time (Net)",
            "record_time": "Cycle Time (Gross)",
            "shift": "Shift",
            "output": "Output",
        }
        colmap.update(toplevelinv)

        table = table.rename(colmap, axis=1)
        return table

    def clean_df_machine_names(self, table):
        """
        Convert the internal machine names to user-facing machine names.
        Function is used to clean up returned results from get_cycle() or get_downtime() query requests.

        :param table: A pandas data table with cycle/machine data
        :type table: class:`DataFrame`

        :return: pandas dataframe
        """

        table = (
            table.copy()
        )  # .loc makes changes to original table, which isn't good.  So operate on a copy.

        # Machines name column may be machine__source or Machine
        if "machine__source" in table.columns:
            machine_field = "machine__source"
        elif "Machine" in table.columns:
            machine_field = "Machine"
        else:
            log.error("Unable to find Machine column to scrub")
            return table

        query_params = {
            "_only": ["source", "source_clean", "source_type"],
            "_order_by": "source_clean",
        }
        mach_names = self.get_machines(**query_params)
        machmap = {
            mach[1]["source"]: mach[1]["source_clean"] for mach in mach_names.iterrows()
        }

        table.loc[:, machine_field] = table[machine_field].apply(
            lambda x: machmap.get(x, x)
        )
        return table

    def clean_query_machine_names(self, query):
        """
        Given a query using the UI friendly machine names, convert them into the Sight Machine expected internal names

        :param query: Dict kwargs passed as part of a query to the API

        :return: dict
        """
        query = query.copy()

        machine_key = (
            "machine__source" if "machine__source" in query else "machine__source__in"
        )

        query_params = {
            "_only": ["source", "source_clean", "source_type"],
            "_order_by": "source_clean",
        }
        mach_names = self.get_machines(**query_params)
        machmap = {
            mach[1]["source_clean"]: mach[1]["source"] for mach in mach_names.iterrows()
        }

        machines = query[machine_key]

        if isinstance(machines, str):
            query[machine_key] = machmap.get(machines, machines)
        else:
            query[machine_key] = [machmap.get(mach, mach) for mach in machines]

        return query

    def clean_query_machine_titles(self, query):
        """
        Given a query for cycles that uses UI friendly tag/field names, convert the machines back into the internal Sight Machine names

        :param query: Dict kwargs passed as part of a query to the API

        :return: dict
        """
        query = query.copy()

        # First need to find the machine name
        machine = query.get("machine__source", query.get("Machine"))
        if isinstance(machine, list):
            # Possible that it is a machine__in.  If so, base on first machine
            machine = query.get("machine__source__in", query.get("Machine__in"))
            machine = machine[0]

        schema = self.get_machine_schema(machine)

        colmap = {row[1]["display"]: row[1]["name"] for row in schema.iterrows()}
        toplevel = {
            "End Time": "endtime",
            "Start Time": "starttime",
            "Machine": "machine__source",
            "Cycle Time (Net)": "total",
            "Cycle Time (Gross)": "record_time",
            "Shift": "shift",
            "Output": "output",
        }
        colmap.update(toplevel)

        translated_query = {}
        for key, val in query.items():
            # Special handling for _order_by since the stat titles are in a list
            if key == "_order_by":
                prefix = ""
                if val.startswith("-"):
                    val = val[1:]
                    prefix = "-"
                val = colmap.get(val, val)

                if val == "endtime":
                    val = "endtime_epoch"
                if val == "starttime":
                    val = "starttime_epoch"

                # For performance, currently only support order by time, machine
                if not val in ["endtime_epoch", "starttime_epoch", "machine__source"]:
                    log.warn(
                        "Only ordering by start time, end time, and machine source currently supported."
                    )
                    continue

                val = f"{prefix}{val}"

            # Special handling for _only
            elif key == "_only":
                # To simplify the logic, always treat as a list of _only items
                if isinstance(val, str):
                    val = [val]

                val = [colmap.get(col, col) for col in val]

            # for all other params
            else:
                func = ""
                if "__" in key:
                    parts = key.split("__")
                    key = "__".join(parts[:-1])
                    func = parts[-1]

                    if not func in [
                        "in",
                        "nin",
                        "gt",
                        "lt",
                        "gte",
                        "lte",
                        "exists",
                        "ne",
                        "eq",
                    ]:
                        # This isn't actually a function.  Probably another nested item like machine__source
                        key = f"{key}__{func}"
                        func = ""

                key = colmap.get(key, key)
                if key in colmap and key not in toplevel:
                    key = f"stats__{key}__val"

                if func:
                    key = f"{key}__{func}"

            translated_query[key] = val

        return translated_query

    def clean_df_downtime_titles(self, table):
        """
        Convert the dataframe column names on Downtime data from the Sight Machine internal name to the user-friendly names.
        Function is used to clean up returned results from get_downtimes() query requests.

        :param table: A pandas data table with cycle or part data
        :type table: class:`DataFrame`
        :return: pandas dataframe
        """

        table = table.rename(downmap, axis=1)
        return table

    def clean_query_downtime_titles(self, query):
        """
        Given a query for downtimes that uses UI friendly tag/field names, convert the machines back into the internal Sight Machine names

        :param query: Dict kwargs passed as part of a query to the API

        :return: dict
        """

        query = query.copy()

        translated_query = {}
        for key, val in query.items():
            # Special handling for _order_by since the stat titles are in a list
            if key == "_order_by":
                prefix = ""
                if val.startswith("-"):
                    val = val[1:]
                    prefix = "-"
                val = downmapinv.get(val, val)

                # For performance, currently only support order by time, machine
                if not val in ["endtime", "starttime", "machine__source"]:
                    log.warn(
                        "Only ordering by start time, end time, and machine source currently supported."
                    )
                    continue

                val = f"{prefix}{val}"

            # Special handling for _only
            elif key == "_only":
                # To simplify the logic, always treat as a list of _only items
                if isinstance(val, str):
                    val = [val]

                val = [downmapinv.get(col, col) for col in val]

            # for all other params
            else:
                func = ""
                if "__" in key:
                    splitted_key = key.split("__")
                    key = "__".join(splitted_key[:-1])
                    func = splitted_key[-1]
                    if not func in [
                        "in",
                        "nin",
                        "gt",
                        "lt",
                        "gte",
                        "lte",
                        "exists",
                        "ne",
                        "eq",
                    ]:
                        # This isn't actually a function.  Probably another nested item like machine__source
                        key = f"{key}__{func}"
                        func = ""

                key = downmapinv.get(key, key)

                if func:
                    key = f"{key}__{func}"

            translated_query[key] = val

        return translated_query

    # DATAVIZ UTILS

    def get_cycle_count(
        self, start_time="", end_time="", field_count=True, machine_type=None
    ):
        """

        Ref: https://sightmachine.atlassian.net/browse/DATA-573
        :param start_time: Starttime from which we want to count cycles default : 1st Jan 2017
        :param end_time: Endtime till we want to count cycles Default : current time
        :param machine_type: machine type
        :return: Dataframe that consists cycle count and column counts
        """

        if not start_time:
            start_time = "2017-01-01T00:00:00"
        if not end_time:
            end_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        column_sequence = [
            "machine_type",
            "source_clean",
            "cycle_count",
            "column_count",
        ]

        cycle_count_schema = {
            "model": "",
            "asset_selection": {
                "machine_source": [],
            },
            "time_selection": {
                "time_type": "absolute",
                "start_time": start_time,
                "end_time": end_time,
            },
        }

        base_url = get_url(
            self.config["protocol"],
            self.tenant,
            self.config["site.domain"],
            self.config["port"],
        )
        cls = smsdkentities.get("dataviz_cycle")(self.session, base_url)

        all_machines = self.get_machines()
        all_machines = all_machines.to_dict("records")
        source_machine_map = {}
        for machine in all_machines:
            if machine["source_type"] not in source_machine_map:
                source_machine_map[machine["source_type"]] = {
                    "source": [machine["source"]],
                    "source_clean": machine["source_clean"],
                }
            else:
                source_machine_map[machine["source_type"]]["source"].append(
                    machine["source"]
                )

        columns = 1  # Default value 1, so will not break any calculation in case field_count=False
        if machine_type and source_machine_map.get(machine_type):
            cycle_count_schema["model"] = "cycle:" + machine_type
            cycle_count_schema["asset_selection"][
                "machine_source"
            ] = source_machine_map[machine_type]["source"]
            cycle_count_records = cls.cycle_count(**cycle_count_schema)
            if field_count:
                schema = self.get_machine_schema(
                    source_machine_map[machine_type]["source"][0]
                )
                columns = schema.shape[0]
            cycle_count_records.update(
                {
                    "machine_type": machine_type,
                    "source_clean": source_machine_map[machine_type]["source_clean"],
                    "column_count": columns,
                }
            )
            return pd.DataFrame([cycle_count_records])

        else:
            cycle_count_records = []
            for machine_type in source_machine_map:
                input_schema = deepcopy(cycle_count_schema)
                input_schema["model"] = "cycle:" + machine_type
                input_schema["asset_selection"]["machine_source"] = source_machine_map[
                    machine_type
                ]["source"]
                records = cls.cycle_count(**input_schema)
                if field_count:
                    schema = self.get_machine_schema(
                        source_machine_map[machine_type]["source"][0]
                    )
                    columns = schema.shape[0]
                records.update(
                    {
                        "machine_type": machine_type,
                        "source_clean": source_machine_map[machine_type][
                            "source_clean"
                        ],
                        "column_count": columns,
                    }
                )
                cycle_count_records.append(records)

            return pd.DataFrame(cycle_count_records, columns=column_sequence)

    def get_all_parts(self, **query):
        all_parts = self.get_data("parts", "get_all_parts", False, **query)
        return all_parts

    def get_part_type_names(self, clean_strings_out=True, query_params=None):
        if query_params is None:
            query_params = {}
        part_types = self.get_data(
            "parts", "get_all_parts", normalize=True, **query_params
        )
        if part_types.empty:
            return pd.DataFrame()
        if clean_strings_out:
            return part_types["part_type_clean"].to_list()
        else:
            return part_types["part_type"].to_list()

    def get_part_count(self, start_time="", end_time="", part_type=None, **kwargs):
        """

        Ref: https://sightmachine.atlassian.net/browse/DATA-573
        :param start_time: Starttime from which we want to count cycles default : 1st Jan 2017
        :param end_time: Endtime till we want to count cycles Default : current time
        :param machine_type: part_type
        :return: Dataframe that consists cycle count and column counts
        """

        if not start_time:
            start_time = "2017-01-01T00:00:00"
        if not end_time:
            end_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        column_sequence = ["part_type", "part_type_clean", "column_count"]

        part_count_schema = {
            "model": "",
            "asset_selection": {},
            "time_selection": {
                "time_type": "absolute",
                "start_time": start_time,
                "end_time": end_time,
            },
        }

        base_url = get_url(
            self.config["protocol"],
            self.tenant,
            self.config["site.domain"],
            self.config["port"],
        )
        cls = smsdkentities.get("dataviz_part")(self.session, base_url)

        all_parts = self.get_all_parts(**kwargs)
        all_parts = all_parts[column_sequence]
        all_parts = all_parts.to_dict("records")
        all_part_types = {i["part_type"]: i["part_type_clean"] for i in all_parts}

        if part_type and (part_type in all_part_types):
            column_count = [
                i["column_count"] for i in all_parts if i["part_type"] == part_type
            ][0]
            part_count_schema["model"] = "part:" + part_type
            part_count_records = cls.part_count(**part_count_schema)
            part_count_records.update(
                {
                    "part_type": part_type,
                    "part_type_clean": all_part_types[part_type],
                    "column_count": column_count,
                }
            )
            return pd.DataFrame([part_count_records])

        else:
            part_count_records = []
            for parts in all_parts:
                part_type = parts["part_type"]
                column_count = [
                    i["column_count"] for i in all_parts if i["part_type"] == part_type
                ][0]

                input_schema = deepcopy(part_count_schema)
                input_schema["model"] = "part:" + part_type
                records = cls.part_count(**input_schema)
                records.update(
                    {
                        "part_type": part_type,
                        "part_type_clean": all_part_types[part_type],
                        "column_count": column_count,
                    }
                )
                part_count_records.append(records)
            column_sequence.append("part_count")
            return pd.DataFrame(part_count_records, columns=column_sequence)

    def get_cycles_batch(
        self,
        query_list,
        normalize=True,
        clean_strings_in=True,
        clean_strings_out=True,
        nodes=4,
    ):
        # https://pathos.readthedocs.io/en/latest/pathos.html
        pool = pathos.pools.ProcessPool(nodes=nodes)
        response = pool.map(
            self.get_cycles,
            [normalize] * len(query_list),
            [clean_strings_in] * len(query_list),
            [clean_strings_out] * len(query_list),
            query_list,
        )
        return response

    def get_downtimes_batch(
        self,
        query_list,
        normalize=True,
        clean_strings_in=True,
        clean_strings_out=True,
        nodes=4,
    ):
        pool = pathos.pools.ProcessPool(nodes=nodes)
        response = pool.map(
            self.get_cycles,
            [normalize] * len(query_list),
            [clean_strings_in] * len(query_list),
            [clean_strings_out] * len(query_list),
            query_list,
        )
        return response

    def get_parts_batch(
        self,
        query_list,
        normalize=True,
        clean_strings_in=True,
        clean_strings_out=True,
        datatab_api=True,
        nodes=4,
    ):
        pool = pathos.pools.ProcessPool(nodes=nodes)
        response = pool.map(
            self.get_parts,
            [normalize] * len(query_list),
            [clean_strings_in] * len(query_list),
            [clean_strings_out] * len(query_list),
            [datatab_api] * len(query_list),
            query_list,
        )
        return response
