#!/usr/bin/env python
# coding: utf-8
""" Sight Machine SDK Client """
from __future__ import unicode_literals, absolute_import

import warnings
import pandas as pd
import re

try:
    from pandas.io.json import json_normalize
except ImportError:
    # for newer pandas versions >1.X
    from pandas import json_normalize

from smsdk.utils import get_url
from smsdk.Auth.auth import Authenticator
from smsdk.tool_register import smsdkentities

import logging
log = logging.getLogger(__name__)

def time_string_to_epoch(time_string):
    try:
        endtime_dt = pd.to_datetime(time_string)
        endtime_epoch = (endtime_dt - pd.to_datetime('1970-01-01')).total_seconds() * 1000 # SM timestamps in ms
    except ValueError as e:
        log.error(f'Unable to parse time string {time_string}: {e}')
        return 0
    except DateParseError as e:
        log.error(f'Bad date specified: {time_string}')
        return 0
    
    return(endtime_epoch)


class Client(object):
    """Easy-to-use client to wrap all SDK functionality."""

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

    def login(self, method, **kwargs):
        """
        Authenticate with the configured tenant and user credentials.

        >>> cli.login('basic', email='user@domain.com', password='password')

        or

        >>> cli.login('apikey', key='YwUuCl7lSP75HcU6GC1Hm5OIXOKcMcSkMEES3_Q1DMU')

        :param method: The authentication method: apikey or basic
        :type method: :class:`string`
        :param kwargs:
            By method:
                * apikey - key
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
        Return the list of egistered entites
        """
        return [e.name for e in smsdkentities.list()]

    def get_data(self, ename, util_name, normalize=False, *args, **kwargs):
        """
        Main data fetching function for all the entities
        :param ename: Name of the entities
        :param util_name: Name of the utility function
        :param normalize: Flatten nested data structures
        from which to retrieve the data
        :return: pandas dataframe
        """
        base_url = get_url(
            self.config["protocol"], self.tenant, self.config["site.domain"]
        )

        df = pd.DataFrame()
        # load the entity class and initialize it
        cls = smsdkentities.get(ename)(self.session, base_url)

        # In the current API, filter by start/endtime + anything else is broken
        # But you can properly filter by epoch + other, so automatically convert those
        for kw in ['endtime', 'endtime__gt', 'endtime__lt', 'starttime', 'starttime__gt', 'starttime__lt']:
            if kw in kwargs:
                original_time = kwargs.pop(kw)
                epoch_time = time_string_to_epoch(original_time)
                new_kw = kw.replace('endtime', 'endtime_epoch').replace('starttime', 'starttime_epoch')
                kwargs[new_kw] = epoch_time
        
        # The current API is inconsistent where most paramters use the MongoEngine-like __ notation for ., but _only requires .
        # So let the user enter '__', but convert those to '.' for API compatibility
        if '_only' in kwargs:
            new_cols = []
            for colname in kwargs.pop('_only'):
                new_cols.append(colname.replace('__', '.'))
            kwargs['_only'] = str(new_cols)


        # check if requested util_name belong the list of
        # registerd utilites
        if util_name in getattr(cls, "get_utilities")(*args, **kwargs):

            # call the utility function
            # all the dict params are passed as kwargs
            # dict params strictly follow {'key':'value'} format
            data = getattr(cls, util_name)(*args, **kwargs)
            
            if normalize:
                # special case to handle the 'stats' block
                if data and 'stats' in data[0]:
                    if isinstance(data[0]['stats'],dict):
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

            if len(df) > 0:
                df.set_index('id', inplace=True)

            # To keep consistent, rename columns back from '.' to '__'
            df.columns = [name.replace('.', '__') for name in df.columns]

        else:
            # raise error if requested for unregistered utility
            raise ValueError("Error - {}".format("Not a registered utility"))
        return df

    # Some shortcut functions
    def get_cycles(self, normalize=False, *args, **kwargs):
        return self.get_data('cycle', 'get_cycles', normalize, *args, **kwargs)

    def get_downtimes(self, normalize=False, *args, **kwargs):
        return self.get_data('downtime', 'get_downtime', normalize, *args, **kwargs)

    def get_machines(self, normalize=False, *args, **kwargs):
        return self.get_data('machine', 'get_machines', normalize, *args, **kwargs)

    def get_machine_names(self):
        query_params = {'_only': ['source', 'source_clean', 'source_type'],
                        '_order_by': 'source_clean'}
        return self.get_data('machine', 'get_machines', normalize=True, **query_params)

    def get_machine_schema(self, machine_source):
    
        try:
            machine_type = self.get_machines(source=machine_source)['source_type'][0]
        except KeyError:
            log.error(f'Unable to find machine type for {machine_source}')
            return

        stats = self.get_machine_types(normalize=False, _limit = 1, source_type = machine_type)['stats'][0]

        fields = []
        for stat in stats:
            if not stat.get('display', {}).get('ui_hidden', False):
                fields.append({'name': stat['analytics']['columns'][0]['name'],
                            'display': stat['display']['title_prefix'],
                            'type': stat['analytics']['columns'][0]['type']})
        return pd.DataFrame(fields)

    def get_machine_types(self, normalize=False, *args, **kwargs):
        return self.get_data('machine_type', 'get_machine_types', normalize, *args, **kwargs)

    def get_parts(self, normalize=False, *args, **kwargs):
        return self.get_data('part', 'get_parts', normalize, *args, **kwargs)
