#!/usr/bin/env python
# coding: utf-8
""" Sight Machine SDK Client """
from __future__ import unicode_literals, absolute_import

import warnings
import pandas as pd

try:
    # for newer pandas versions >1.X
    from pandas import json_normalize
except ImportError:
    from pandas.io.json import json_normalize

from smsdk.utils import get_url
from smsdk.Auth.auth import Authenticator
from smsdk.tool_register import smsdkentities

import logging
log = logging.getLogger(__name__)

def time_string_to_epoch(time_string):
    try:
        dt = pd.to_datetime(time_string)
        time_epoch = (dt - pd.to_datetime('1970-01-01')).total_seconds() * 1000 # SM timestamps in ms
    except ValueError as e:
        log.error(f'Unable to parse time string {time_string}: {e}')
        return 0
    except Exception as e:
        log.error(f'Bad date specified: {time_string}')
        return 0
    
    return(time_epoch)


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

        >>> cli.login('apikey', key_id='api_key_string', secret_id='api_secret_string')

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
        Return the list of egistered entites
        """
        return [e.name for e in smsdkentities.list()]

    def get_data(self, ename, util_name, normalize=True, *args, **kwargs):
        """
        Main data fetching function for all the entities.  Note this is the general data fetch function.  You probably want to use the model-specific functions such as get_cycles().
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
        for kw in ['endtime', 'endtime__gt', 'endtime__lt', 'endtime__gte', 'endtime__lte', 'starttime', 'starttime__gt', 'starttime__lt''starttime__gte', 'starttime__lte']:
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

        # Fix format for __in commands
        for key, val in kwargs.items():
            if '__in' in key:
                kwargs[key] = str(val)

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
    def get_cycles(self, normalize=True, clean_strings_in=True, clean_strings_out=True, *args, **kwargs):
        """
        Shortcut for retreiving cycle/machine data.  Pull data from the cycle model and cleans up headers, machine names
        :param normalize: Flatten nested data structures
        from which to retrieve the data
        :param clean_strings_in: Convert the UI-based names into the internal database names.
        :param clean_strings_out: Replace Sight Machine internal column and machine names with user-facing names. 
        :return: pandas dataframe
        """
        
        if not '_only' in kwargs:
            machine = kwargs.get('machine__source', kwargs.get('Machine'))
            if not machine:
            # Possible that it is a machine__in.  If so, base on first machine
                machine = kwargs.get('machine__source__in', kwargs.get('Machine__in'))
                machine = machine[0]

            schema = self.get_machine_schema(machine)['name'].tolist()
            toplevel = ['machine__source', 'starttime', 'endtime', 'total', 'record_time', 'shift', 'output']

            kwargs['_only'] = schema + toplevel

        if clean_strings_in:
            kwargs = self.clean_query_machine_titles(kwargs)
            kwargs = self.clean_query_machine_names(kwargs)
        
        df = self.get_data('cycle', 'get_cycles', normalize, *args, **kwargs)

        if len(df) > 0 and clean_strings_out:
            df = self.clean_df_machine_titles(df)
            df = self.clean_df_machine_names(df)

        return df

    def get_downtimes(self, normalize=True, clean_strings_in=True, clean_strings_out=True, *args, **kwargs):
        """
        Get Downtime data.
        :param normalize: Flatten nested data structures
        :param clean_strings_in: Convert the UI-based names into the internal database names.
        :param clean_strings_out: Replace Sight Machine internal column and machine names with user-facing names. 
        :return: pandas dataframe
        """

        if not '_only' in kwargs:
            kwargs['_only'] = downmap.keys()

        if clean_strings_in:
            kwargs = self.clean_query_downtime_titles(kwargs)
            kwargs = self.clean_query_machine_names(kwargs)
        
        df = self.get_data('downtime', 'get_downtime', normalize, *args, **kwargs)

        if clean_strings_out:
            df = self.clean_df_downtime_titles(df)
            df = self.clean_df_machine_names(df)
            
        return df

    def get_downtimes_with_cycles(self, normalize=True, clean_strings_in=True, clean_strings_out=True, *args, **kwargs):
        """
        Merges cycle and downtime data where each downtime record also has its preceeding cycle stats.  Parameters are 
        identical to get_downtimes(), but the returned data structure will also have corresponding cycle data.

        Note this function takes time as it is handling many queries to assemble the resulting data frame.

        :param normalize: Flatten nested data structures
        :param clean_strings_in: Convert the UI-based names into the internal database names.
        :param clean_strings_out: Replace Sight Machine internal column and machine names with user-facing names. 
        :return: pandas dataframe
        """

        df = self.get_downtimes(normalize = normalize, clean_strings_in=clean_strings_in, clean_strings_out=clean_strings_out, **kwargs)

        # Get the cycle before each downtime record
        cycs = []
        for row in df.iterrows():
            query = {'machine__source': row[1].get('Machine', row[1].get('machine__source')),
                    'starttime__lte': row[1].get('Start Time', row[1].get('starttime')),
                    '_limit': 1,
                    '_order_by': '-starttime'}
            cycs.append(self.get_cycles(clean_strings_in=clean_strings_in, clean_strings_out=clean_strings_out, **query))
        df_cyc = pd.concat(cycs)

        # Just joining by row, so reset all the indexes to just the row number and get rid of the mongo object id
        df = df.reset_index()
        df = df.drop('id', axis = 1)
        df_cyc = df_cyc.reset_index()
        if clean_strings_out:
            df_cyc = df_cyc.drop(['Machine', 'id', 'Shift'], axis = 1) # Also get rid of fields that are duplicate on both downtime and cycle
            df_cyc = df_cyc.rename({'Start Time': 'Cycle Start Time', 'End Time': 'Cycle End Time'}, axis = 1)  # Retitle times so clear these are from the cycle
        else:
            df_cyc = df_cyc.drop(['machine__source', 'id', 'shift'], axis = 1) # Also get rid of fields that are duplicate on both downtime and cycle
            df_cyc = df_cyc.rename({'starttime': 'cycle_starttime', 'End Time': 'cycle_endtime'}, axis = 1)  # Retitle times so clear these are from the cycle
                
        merged = df.merge(df_cyc, left_index = True, right_index = True)

        return merged

    def get_machines(self, normalize=True, *args, **kwargs):
        """
        Get list of machines and associated metadata.  Note this includes extensive internal metadata.  Most use cases will likely want get_machine_names(). 
        :param normalize: Flatten nested data structures
        :return: pandas dataframe
        """
        return self.get_data('machine', 'get_machines', normalize, *args, **kwargs)

    def get_machine_names(self, source_type = None, clean_strings_out=True):
        """
        Get a list of machines.  

        :param source_type: filter the list to only the specified source_type
        :param clean_strings_out: If true, return the list using the Machine's UI name.  If false, the list contains internal machine names.
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
                    source_type = mt['source_type'][0]
                else:
                    log.error('Machine Type not found')
                    return []
            
            query_params['source_type'] = source_type


        machines = self.get_data('machine', 'get_machines', normalize=True, **query_params)

        if clean_strings_out:
            return machines['source_clean'].to_list()
        else:
            return machines['source'].to_list()
        

    def get_machine_schema(self, machine_source, types = []):
        """
        Get a list of fields/tags on a given machine

        :param machine_source: the name of the machine to get the list of tags for.
        :param types: an option list of data types (float, int, string, boolean) to filter the list of fields based on their data type.
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

        stats = self.get_machine_types(normalize=False, _limit = 1, source_type = machine_type)['stats'][0]

        fields = []
        for stat in stats:
            if not stat.get('display', {}).get('ui_hidden', False):
                if len(types) == 0 or stat['analytics']['columns'][0]['type'] in types:
                    fields.append({'name': f'stats__{stat["title"]}__val',
                                   #'name': stat['analytics']['columns'][0]['name'],
                                   'display': stat['display']['title_prefix'],
                                   'type': stat['analytics']['columns'][0]['type']})
        return pd.DataFrame(fields)

    def get_machine_types(self, normalize=True, *args, **kwargs):
        return self.get_data('machine_type', 'get_machine_types', normalize, *args, **kwargs)

    def get_machine_type_names(self, clean_strings_out=True):
        query_params = {'_only': ['source_type', 'source_type_clean'],
                        '_order_by': 'source_type_clean'}
        machine_types = self.get_data('machine_type', 'get_machine_types', normalize=True, **query_params)

        if clean_strings_out:
            return machine_types['source_type_clean'].to_list()
        else:
            return machine_types['source_type'].to_list()

    def get_parts(self, normalize=True, *args, **kwargs):
        return self.get_data('part', 'get_parts', normalize, *args, **kwargs)

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
                machine = table.loc[:, 'machine__source'][0]
            except KeyError as e:
                try:
                    # Maybe it was already cleaned
                    machine = table.loc[:, 'Machine'][0]
                except KeyError as e:
                    log.error(f'Unable to lookup source type for schema: {e}')
                    return table
            
        schema = self.get_machine_schema(machine)

        colmap = {row[1]['name']: row[1]['display'] for row in schema.iterrows()}
        toplevelinv = {'endtime': 'End Time',
                       'starttime': 'Start Time',
                       'machine__source': 'Machine',
                       'total': 'Cycle Time (Net)', 
                       'record_time': 'Cycle Time (Gross)', 
                       'shift': 'Shift', 
                       'output': 'Output'}
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

        table = table.copy() #.loc makes changes to original table, which isn't good.  So operate on a copy.

        # Machines name column may be machine__source or Machine
        if 'machine__source' in table.columns:
            machine_field = 'machine__source'
        elif 'Machine' in table.columns:
            machine_field = 'Machine'
        else:
            log.error('Unable to find Machine column to scrub')
            return table

        query_params = {'_only': ['source', 'source_clean', 'source_type'],
                        '_order_by': 'source_clean'}
        mach_names = self.get_machines(**query_params)
        machmap = {mach[1]['source']: mach[1]['source_clean'] for mach in mach_names.iterrows()}

        table.loc[:, machine_field] = table[machine_field].apply(lambda x: machmap.get(x, x))
        return table

    def clean_query_machine_names(self, query):
        """
        Given a query using the UI friendly machine names, convert them into the Sight Machine expected internal names

        :param query: Dict kwargs passed as part of a query to the API
        
        :return: dict
        """
        query = query.copy()
        
        machine_key = 'machine__source' if 'machine__source' in query else 'machine__source__in'
        
        query_params = {'_only': ['source', 'source_clean', 'source_type'],
                        '_order_by': 'source_clean'}
        mach_names = self.get_machines(**query_params)
        machmap = {mach[1]['source_clean']: mach[1]['source'] for mach in mach_names.iterrows()}

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
        machine = query.get('machine__source', query.get('Machine'))
        if not machine:
        # Possible that it is a machine__in.  If so, base on first machine
            machine = query.get('machine__source__in', query.get('Machine__in'))
            machine = machine[0]

        schema = self.get_machine_schema(machine)

        colmap = {row[1]['display']: row[1]['name'] for row in schema.iterrows()}
        toplevel = {'End Time': 'endtime',
                    'Start Time': 'starttime',
                    'Machine': 'machine__source',
                    'Cycle Time (Net)': 'total', 
                    'Cycle Time (Gross)': 'record_time', 
                    'Shift': 'shift', 
                    'Output': 'output'}
        colmap.update(toplevel)
    
        translated_query = {}
        for key, val in query.items():
            
            # Special handling for _order_by since the stat titles are in a list
            if key == '_order_by':
                
                prefix = ''
                if val.startswith('-'):
                    val = val[1:]
                    prefix = '-'
                val = colmap.get(val, val)
                
                # For performance, currently only support order by time, machine
                if not val in ['endtime', 'starttime', 'machine__source']:
                    log.warn('Only ordering by start time, end time, and machine source currently supported.')
                    continue

                val = f'{prefix}{val}'
                
            # Special handling for _only
            elif key == '_only':
                # To simplify the logic, always treat as a list of _only items 
                if isinstance(val, str):
                    val = [val]

                val = [colmap.get(col, col) for col in val]

            #for all other params
            else: 
                func = ''
                if '__' in key:
                    key, func = key.split('__')
                    if not func in ['in', 'nin', 'gt', 'lt', 'gte', 'lte', 'exists', 'ne', 'eq']:
                        # This isn't actually a function.  Probably another nested item like machine__source
                        key = f'{key}__{func}'
                        func = ''
                        
                key = colmap.get(key, key)
                if key in colmap and key not in toplevel:
                    key = f'stats__{key}__val'
                
                if func:
                    key = f'{key}__{func}'
                
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
        return(table)
        
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
            if key == '_order_by':
                
                prefix = ''
                if val.startswith('-'):
                    val = val[1:]
                    prefix = '-'
                val = downmapinv.get(val, val)
                
                # For performance, currently only support order by time, machine
                if not val in ['endtime', 'starttime', 'machine__source']:
                    log.warn('Only ordering by start time, end time, and machine source currently supported.')
                    continue

                val = f'{prefix}{val}'
                
            # Special handling for _only
            elif key == '_only':
                # To simplify the logic, always treat as a list of _only items 
                if isinstance(val, str):
                    val = [val]

                val = [downmapinv.get(col, col) for col in val]

            #for all other params
            else: 
                func = ''
                if '__' in key:
                    key, func = key.split('__')
                    if not func in ['in', 'nin', 'gt', 'lt', 'gte', 'lte', 'exists', 'ne', 'eq']:
                        # This isn't actually a function.  Probably another nested item like machine__source
                        key = f'{key}__{func}'
                        func = ''
                        
                key = downmapinv.get(key, key)
                
                if func:
                    key = f'{key}__{func}'
                
            translated_query[key] = val

        return translated_query
