#!/usr/bin/env python
# coding: utf-8
""" Sight Machine SDK Client """
from __future__ import unicode_literals, absolute_import

import warnings
import pandas as pd

try:
    from pandas.io.json import json_normalize
except ImportError:
    # for newer pandas versions >1.X
    from pandas import json_normalize

from smsdk.utils import get_url
from smsdk.Auth.auth import Authenticator
from smsdk.tool_register import smsdkentities


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
        from which to retrieve the data
        :return: pandas dataframe
        """
        base_url = get_url(
            self.config["protocol"], self.tenant, self.config["site.domain"]
        )

        df = pd.DataFrame()
        # load the entity class and initialize it
        cls = smsdkentities.get(ename)(self.session, base_url)

        # check if requested util_name belong the list of
        # registerd utilites
        if util_name in getattr(cls, "get_utilities")(*args, **kwargs):

            # warn message if enable_pagination and limit used together
            if "enable_pagination" in kwargs and "_limit" in kwargs:
                msg = "WARNING: enable_pagination overrides the _limit"
                warnings.warn(msg, RuntimeWarning)

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
        else:
            # raise error if requested for unregistered utility
            raise ValueError("Error - {}".format("Not a registered utility"))
        return df
