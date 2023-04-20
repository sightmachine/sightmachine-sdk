#!/usr/bin/env python
# coding: utf-8
""" Sight Machine SDK Client """
from __future__ import unicode_literals, absolute_import

import pandas as pd

try:
    # for newer pandas versions >1.X
    from pandas import json_normalize
except ImportError:
    from pandas.io.json import json_normalize

from smsdk.utils import get_url
from smsdk.Auth.auth import Authenticator, X_SM_DB_SCHEMA
from smsdk.tool_register import smsdkentities
from smsdk.client_v0 import ClientV0

import logging

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


# We don't have a downtime schema, so hard code one
downmap = {
    "machine__source": "Machine",
    "starttime": "Start Time",
    "endtime": "End Time",
    "total": "Duration",
    "shift": "Shift",
    "metadata__reason": "Downtime Reason",
    "metadata__category": "Downtime Category",
    "metadata__downtime_type": "Downtime Type",
}

downmapinv = {
    "Machine": "machine__source",
    "Start Time": "starttime",
    "End Time": "endtime",
    "Duration": "total",
    "Shift": "shift",
    "Downtime Reason": "metadata__reason",
    "Downtime Category": "metadata__category",
    "Downtime Type": "metadata__downtime_type",
}


class Client(ClientV0):
    """Connection point to the Sight Machine platform to retrieve data"""

    session = None
    tenant = None
    config = None

    def __init__(self, tenant, site_domain="sightmachine.io", protocol="https"):
        """
        Initialize the client.

        :param tenant: The tenant within Sight Machine to access.
        :type tenant: :class:`string`
        :param site_domain:
            The site domain to connect to. Necessary to change if deploying in
            a non-standard environment.
        :type site_domain: :class:`string`
        """

        self.tenant = tenant

        # Handle internal configuration
        self.config = {}
        self.config["protocol"] = protocol
        self.config["site.domain"] = site_domain

        # Setup Authenticator
        self.auth = Authenticator(self)
        self.session = self.auth.session

    def select_db_schema(self, schema_name):
        self.session.headers.update({X_SM_DB_SCHEMA: schema_name})

    def get_data_v1(self, ename, util_name, normalize=True, *args, **kwargs):
        """
        Main data fetching function for all the entities.  Note this is the general data fetch function.  You probably want to use the model-specific functions such as get_cycles().
        :param ename: Name of the entities
        :param util_name: Name of the utility function
        :param normalize: Flatten nested data structures
        :return: pandas dataframe
        """
        base_url = get_url(
            self.config["protocol"], self.tenant, self.config["site.domain"]
        )

        df = pd.DataFrame()
        # load the entity class and initialize it
        cls = smsdkentities.get(ename)(self.session, base_url)

        # The current API is inconsistent where most paramters use the MongoEngine-like __ notation for ., but _only requires .
        # So let the user enter '__', but convert those to '.' for API compatibility
        # if '_only' in kwargs:
        #     new_cols = []
        #     for colname in kwargs.pop('_only'):
        #         new_cols.append(colname.replace('__', '.'))
        #     kwargs['_only'] = new_cols

        # Fix format for __in commands
        # for key, val in kwargs.items():
        #    if '__in' in key:
        #        kwargs[key] = str(val)

        # check if requested util_name belong the list of
        # registerd utilites
        if util_name in getattr(cls, "get_utilities")(*args, **kwargs):
            # call the utility function
            # all the dict params are passed as kwargs
            # dict params strictly follow {'key':'value'} format

            # sub_kwargs = kwargs
            if util_name in ["get_cycles", "get_downtime", "get_parts"]:
                sub_kwargs = [kwargs]
            else:
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

    @ClientV0.validate_input
    @ClientV0.cycle_decorator
    def get_cycles(
        self,
        normalize=True,
        clean_strings_in=True,
        clean_strings_out=True,
        *args,
        **kwargs,
    ):
        df = self.get_data_v1("cycle_v1", "get_cycles", normalize, *args, **kwargs)

        return df

    @ClientV0.validate_input
    @ClientV0.downtime_decorator
    def get_downtimes(
        self,
        normalize=True,
        clean_strings_in=True,
        clean_strings_out=True,
        *args,
        **kwargs,
    ):
        df = self.get_data_v1("downtime_v1", "get_downtime", normalize, *args, **kwargs)

        return df

    @ClientV0.validate_input
    @ClientV0.part_decorator
    def get_parts(
        self,
        normalize=True,
        clean_strings_in=True,
        clean_strings_out=True,
        datatab_api=True,
        *args,
        **kwargs,
    ):
        df = self.get_data_v1("part_v1", "get_parts", normalize, *args, **kwargs)

        return df

    def get_kpis(self, **kwargs):
        kpis = smsdkentities.get("kpi")
        base_url = get_url(
            self.config["protocol"], self.tenant, self.config["site.domain"]
        )
        return kpis(self.session, base_url).get_kpis(**kwargs)

    def get_kpis_for_asset(self, **kwargs):
        kpis = smsdkentities.get("kpi")
        base_url = get_url(
            self.config["protocol"], self.tenant, self.config["site.domain"]
        )
        return kpis(self.session, base_url).get_kpis_for_asset(**kwargs)

    def get_kpi_data_viz(
        self,
        machine_sources=None,
        kpis=None,
        i_vars=None,
        time_selection=None,
        **kwargs,
    ):
        kpi_entity = smsdkentities.get("kpi")
        if machine_sources:
            machine_types = []
            for machine_source in machine_sources:
                machine_types.append(
                    self.get_type_from_machine(machine_source, **kwargs)
                )
            kwargs["asset_selection"] = {
                "machine_source": machine_sources,
                "machine_type": list(set(machine_types)),
            }

        if kpis:
            d_vars = []
            for kpi in kpis:
                d_vars.append({"name": kpi, "aggregate": ["avg"]})
            kwargs["d_vars"] = d_vars

        if i_vars:
            kwargs["i_vars"] = i_vars

        if time_selection:
            kwargs["time_selection"] = time_selection

        base_url = get_url(
            self.config["protocol"], self.tenant, self.config["site.domain"]
        )
        return kpi_entity(self.session, base_url).get_kpi_data_viz(**kwargs)

    def get_type_from_machine(self, machine_source=None, **kwargs):
        machine = smsdkentities.get("machine")
        base_url = get_url(
            self.config["protocol"], self.tenant, self.config["site.domain"]
        )
        return machine(self.session, base_url).get_type_from_machine_name(
            machine_source, **kwargs
        )

    def get_machine_schema(
        self, machine_source, types=[], show_hidden=False, return_mtype=False, **kwargs
    ):
        machineType = smsdkentities.get("machine_type")
        machine_type = self.get_type_from_machine(machine_source)
        base_url = get_url(
            self.config["protocol"], self.tenant, self.config["site.domain"]
        )
        fields = machineType(self.session, base_url).get_fields(machine_type, **kwargs)
        fields = [
            field for field in fields if not field.get("ui_hidden") or show_hidden
        ]
        if len(types) > 0:
            fields = [field for field in fields if field.get("type") in types]

        frame = pd.DataFrame(fields).rename(
            columns={
                "display_name": "display",
                "type": "sight_type",
                "data_type": "type",
            }
        )

        if return_mtype:
            return (machine_type, frame)

        return frame

    def get_fields_of_machine_type(
        self, machine_type, types=[], show_hidden=False, **kwargs
    ):
        machineType = smsdkentities.get("machine_type")
        base_url = get_url(
            self.config["protocol"], self.tenant, self.config["site.domain"]
        )
        fields = machineType(self.session, base_url).get_fields(machine_type, **kwargs)
        fields = [
            field for field in fields if not field.get("ui_hidden") or show_hidden
        ]
        if len(types) > 0:
            fields = [field for field in fields if field.get("type") in types]

        return fields

    def get_cookbooks(self, **kwargs):
        """
        Gets all of the cookbooks accessable to the logged in user.
        :return: list of cookbooks
        """
        cookbook = smsdkentities.get("cookbook")
        base_url = get_url(
            self.config["protocol"], self.tenant, self.config["site.domain"]
        )
        return cookbook(self.session, base_url).get_cookbooks(**kwargs)

    def get_cookbook_top_results(self, recipe_group_id, limit=10, **kwargs):
        """
        Gets the top runs for a recipe group.
        :param recipe_group_id: The id of the recipe group to get runs for.
        :param limit: The max number of runs wished to return.  Defaults to 10.
        :return: List of runs
        """
        cookbook = smsdkentities.get("cookbook")
        base_url = get_url(
            self.config["protocol"], self.tenant, self.config["site.domain"]
        )
        return cookbook(self.session, base_url).get_top_results(
            recipe_group_id, limit, **kwargs
        )

    def get_cookbook_current_value(self, variables=[], minutes=1440, **kwargs):
        """
        Gets the current value of a field.
        :param variables: A list of fields to return values for in the format {'asset': machine_name, 'name': field_name}
        :param minutes: The number of minutes to consider when grabing the current value, defaults to 1440 or 1 day
        :return: A list of values associated with the proper fields.
        """
        cookbook = smsdkentities.get("cookbook")
        base_url = get_url(
            self.config["protocol"], self.tenant, self.config["site.domain"]
        )
        return cookbook(self.session, base_url).get_current_value(
            variables, minutes, **kwargs
        )

    def normalize_constraint(self, constraint):
        """
        Takes a constraint and returns a string version of it's to and from fields.
        :param constraint: A range constraint field most have a to and from key.
        :return: A string
        """
        to = constraint.get("to")
        from_constraint = constraint.get("from")
        return "({},{})".format(to, from_constraint)

    def normalize_constraints(self, constraints):
        """
        Takes a list of constraint and returns string versions of their to and from fields.
        :param constraint: A list range constraint field each most have a to and from key.
        :return: A list of strings
        """
        constraints_normal = []
        for constraint in constraints:
            constraints_normal.append(self.normalize_constraint(constraint))
        return constraints_normal

    def get_lines(self, **kwargs):
        """
        Returns all the lines for the facility
        """
        lines = smsdkentities.get("line")
        base_url = get_url(
            self.config["protocol"], self.tenant, self.config["site.domain"]
        )
        return lines(self.session, base_url).get_lines(**kwargs)

    one_day_relative = {
        "time_type": "relative",
        "relative_start": 1,
        "relative_unit": "day",
        "ctime_tz": "America/Los_Angeles",
    }

    def get_line_data(
        self,
        assets,
        fields=[],
        time_selection=one_day_relative,
        asset_time_offset={},
        filters=[],
        limit=400,
        offset=0,
        **kwargs,
    ):
        """
        Returns all the lines for the facility
        :param assets: A list of assets you wish to get data for
        :param asset_time_offset: A dictionary of the time offsets to use for assets
        :param fields: A list of dicts that has the asset and name of fields you wish to select
        :param time_selection: A time selection for your query defaults to one day relative
        :param filter: A list of filters on the data
        :param limit: A limit of records to grab defaults to 400
        :param offset: The offset to start the data at
        """
        lines = smsdkentities.get("line")
        base_url = get_url(
            self.config["protocol"], self.tenant, self.config["site.domain"]
        )

        asset_selection = []
        for asset in assets:
            asset_selection.append({"asset": asset})
            if asset_time_offset.get(asset) == None:
                asset_time_offset[asset] = {"interval": 0, "period": "minutes"}
        where = []
        if len(filters) > 0:
            for filter in filters:
                where.append({"nested": [filter]})

        kwargs["asset_selection"] = asset_selection
        kwargs["asset_time_offset"] = asset_time_offset
        kwargs["select"] = fields
        kwargs["time_selection"] = time_selection
        kwargs["db_mode"] = "sql"
        kwargs["model"] = "line"
        kwargs["model_type"] = "data-table"
        kwargs["where"] = where

        return lines(self.session, base_url).get_line_data(
            limit=limit, offset=offset, **kwargs
        )
