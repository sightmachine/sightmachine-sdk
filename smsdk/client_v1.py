#!/usr/bin/env python
# coding: utf-8
""" Sight Machine SDK Client """
from __future__ import unicode_literals, absolute_import

import numpy as np
import pandas as pd

try:
    # for newer pandas versions >1.X
    from pandas import json_normalize
except ImportError:
    from pandas.io.json import json_normalize

from smsdk.utils import get_url
from smsdk.Auth.auth import Authenticator
from smsdk.tool_register import smsdkentities
from smsdk.client import Client

import logging

log = logging.getLogger(__name__)


def time_string_to_epoch(time_string):
    try:
        dt = pd.to_datetime(time_string)
        time_epoch = (dt - pd.to_datetime('1970-01-01')).total_seconds() * 1000  # SM timestamps in ms
    except ValueError as e:
        log.error(f'Unable to parse time string {time_string}: {e}')
        return 0
    except Exception as e:
        log.error(f'Bad date specified: {time_string}')
        return 0

    return (time_epoch)


def dict_to_df(data, normalize=True):
    if normalize:
        # special case to handle the 'stats' block
        if data and 'stats' in data[0]:
            if isinstance(data[0]['stats'], dict):
                # part stats are dict
                df = json_normalize(data)
            else:
                # machine type stats are list
                cols = [*data[0]]
                cols.remove('stats')
                df = json_normalize(data, 'stats', cols, record_prefix='stats.')
        else:
            df = json_normalize(data)
    else:
        df = pd.DataFrame(data)

    # if len(df) > 0:
    #     df.set_index('_id', inplace=True)

    return df


# We don't have a downtime schema, so hard code one
downmap = {'machine__source': 'Machine',
           'starttime': 'Start Time',
           'endtime': 'End Time',
           'total': 'Duration',
           'shift': 'Shift',
           'metadata__reason': 'Downtime Reason',
           'metadata__category': 'Downtime Category',
           'metadata__downtime_type': 'Downtime Type'}

downmapinv = {'Machine': 'machine__source',
              'Start Time': 'starttime',
              'End Time': 'endtime',
              'Duration': 'total',
              'Shift': 'shift',
              'Downtime Reason': 'metadata__reason',
              'Downtime Category': 'metadata__category',
              'Downtime Type': 'metadata__downtime_type'}


class ClientV1(Client):
    """Connection point to the Sight Machine platform to retrieve data"""

    session = None
    tenant = None
    config = None

    def __init__(self, tenant, site_domain="sightmachine.io"):
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
        self.config["protocol"] = "https"
        self.config["site.domain"] = site_domain

        # Setup Authenticator
        self.auth = Authenticator(self)
        self.session = self.auth.session

    def get_data(self, ename, util_name, normalize=True, *args, **kwargs):

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
        for key, val in kwargs.items():
            if '__in' in key:
                kwargs[key] = str(val)

        # check if requested util_name belong the list of
        # registerd utilites
        print(f"UTILS----{util_name}")
        if util_name in getattr(cls, "get_utilities")(*args, **kwargs):

            # call the utility function
            # all the dict params are passed as kwargs
            # dict params strictly follow {'key':'value'} format

            # sub_kwargs = kwargs
            if util_name == 'get_cycles':
                sub_kwargs = [kwargs]
            else:
                sub_kwargs = self.fix_only(kwargs)

            if len(sub_kwargs) == 1:
                data = dict_to_df(getattr(cls, util_name)(*args, **sub_kwargs[0]), normalize)
            else:
                data = dict_to_df(getattr(cls, util_name)(*args, **sub_kwargs[0]), normalize)
                for sub in sub_kwargs[1:]:
                    sub_data = dict_to_df(getattr(cls, util_name)(*args, **sub), normalize)
                    data = data.join(sub_data, rsuffix='__joined')
                    joined_cols = [col for col in data.columns if '__joined' in col]
                    data.drop(joined_cols, axis=1)

            # To keep consistent, rename columns back from '.' to '__'
            data.columns = [name.replace('.', '__') for name in data.columns]

        else:
            # raise error if requested for unregistered utility
            raise ValueError("Error - {}".format("Not a registered utility"))

        if 'endtime' in data.columns:
            data['endtime'] = pd.to_datetime(data['endtime'])
        if 'starttime' in data.columns:
            data['starttime'] = pd.to_datetime(data['starttime'])

        return data

    def get_cycles(self, normalize=True, clean_strings_in=True, clean_strings_out=True, *args, **kwargs):
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


        if not '_only' in kwargs:
            print('_only not specified.  Selecting first 50 fields.')
            machine = kwargs.get('machine__source', kwargs.get('Machine'))
            if not machine:
                # Possible that it is a machine__in.  If so, base on first machine
                machine = kwargs.get('machine__source__in', kwargs.get('Machine__in'))
                machine = machine[0]
            schema = self.get_machine_schema(machine)
            schema = schema['name'].tolist()[:50]
            toplevel = ['machine__source', 'starttime', 'endtime', 'total', 'record_time', 'shift', 'output']

            kwargs['_only'] = schema + toplevel

        # if kwargs['_only'] == '*':
        #     kwargs.pop('_only')
        #
        # if clean_strings_in:
        #     kwargs = self.clean_query_machine_titles(kwargs)
        #     kwargs = self.clean_query_machine_names(kwargs)

        df = self.get_data('cycle_v2', 'get_cycles', normalize, *args, **kwargs)

        if len(df) > 0 and clean_strings_out:
            df = self.clean_df_machine_titles(df)
            df = self.clean_df_machine_names(df)

        return df

    def get_machines(self, normalize=True, *args, **kwargs):
        """
        Get list of machines and associated metadata.  Note this includes extensive internal metadata.  If you only want to get a list of machine names
        then see also get_machine_names().

        :param normalize: Flatten nested data structures
        :type normalize: bool
        :return: pandas dataframe
        """
        return self.get_data('machine', 'get_machines', normalize, *args, **kwargs)

    def get_machine_names(self, source_type=None, clean_strings_out=True):
        """
        Get a list of machine names.  This is a simplified version of get_machines().

        :param source_type: filter the list to only the specified source_type
        :type source_type: str
        :param clean_strings_out: If true, return the list using the UI-based display names.  If false, the list contains the Sight Machine internal machine names.
        :return: list
        """

        query_params = {'_only': ['source', 'source_clean', 'source_type'],
                        '_order_by': 'source_clean'}

        if source_type:
            # Double check the type
            mt = self.get_machine_types(source_type=source_type)
            # If it was found, then no action to take, otherwise try looking up from clean string
            if not len(mt):
                mt = self.get_machine_types(source_type_clean=source_type)
                if len(mt):
                    source_type = mt['source_type'].iloc[0]
                else:
                    log.error('Machine Type not found')
                    return []

            query_params['source_type'] = source_type

        machines = self.get_data('machine', 'get_machines', normalize=True, **query_params)

        if clean_strings_out:
            return machines['source_clean'].to_list()
        else:
            return machines['source'].to_list()

    def get_machine_schema(self, machine_source, types=[]):
        """
        Get a list of fields/tags on a given machine, including the Sight Machine internal name, UI display name, and data type.

        :param machine_source: the name of the machine to get the list of tags for.
        :type machine_source: str
        :param types: an optional list of strings of the type to filter the list of fields based on their data type.  Allowed options are float, int, string, boolean.
        :type types: list
        :return: pandas dataframe
        """

        try:
            machine_type = self.get_machines(source=machine_source)['source_type'][0]
        except KeyError:
            try:
                # Possible that this was done on a clean string
                machine_type = self.get_machines(source_clean=machine_source)['source_type'][0]
            except KeyError:
                log.error(f'Unable to find machine type for {machine_source}')
                return

        stats = self.get_machine_types(normalize=False, _limit=1, source_type=machine_type)['stats'][0]

        fields = []
        for stat in stats:
            if not stat.get('display', {}).get('ui_hidden', False):
                if len(types) == 0 or stat['analytics']['columns'][0]['type'] in types:
                    fields.append({'name': f'stats__{stat["title"]}__val',
                                   # 'name': stat['analytics']['columns'][0]['name'],
                                   'display': stat['display']['title_prefix'],
                                   'type': stat['analytics']['columns'][0]['type']})
        return pd.DataFrame(fields)

    def get_machine_types(self, normalize=True, *args, **kwargs):
        """
        Get list of machine types and associated metadata.  Note this includes extensive internal metadata.  If you only want to get a list of machine type names
        then see also get_machine_type_names().

        :param normalize: Flatten nested data structures
        :type normalize: bool
        :return: pandas dataframe
        """

        return self.get_data('machine_type', 'get_machine_types', normalize, *args, **kwargs)

    def get_machine_type_names(self, clean_strings_out=True):
        """
        Get a list of machine type names.  This is a simplified version of get_machine_types().

        :param clean_strings_out: If true, return the list using the UI-based display names.  If false, the list contains the Sight Machine internal machine types.
        :return: list
        """
        query_params = {'_only': ['source_type', 'source_type_clean'],
                        '_order_by': 'source_type_clean'}
        machine_types = self.get_data('machine_type', 'get_machine_types', normalize=True, **query_params)

        if clean_strings_out:
            return machine_types['source_type_clean'].to_list()
        else:
            return machine_types['source_type'].to_list()
