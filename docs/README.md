# All Functions

This document provides an overview of the various functions available in the Sight Machine SDK. These functions are designed to help you interact with and retrieve data from the Sight Machine platform efficiently. Each function is accompanied by example code snippets to demonstrate their usage and to help you integrate them into your own applications. 

Functions are split into general functions which pull general factory metadata, and data queries which pull tabular data from the various data models. All functions are methods of the client object, which needs to be instantiated first.


## Table of Contents

- [Instantiate Client](#instantiate-client)
- [General Metadata Functions](#general-metadata-functions)
  - [Machine Type Info](#machine-type-info)
    - [Client.get_machine_types](#clientget_machine_types)
    - [Client.get_machine_type_names](#clientget_machine_type_names)
    - [Client.get_fields_of_machine_type](#clientget_fields_of_machine_type)
  - [Machine Info](#machine-info)
    - [Client.get_machines](#clientget_machines)
    - [Client.get_machine_names](#clientget_machine_names)
    - [Client.get_machine_schema](#clientget_machine_schema)
    - [Client.get_type_from_machine](#clientget_type_from_machine)
  - [Other](#other)
    - [Client.get_lines](#clientget_lines)
    - [Client.get_machine_timezone](#clientget_machine_timezone)
    - [Client.create_share_link](#clientcreate_share_link)
    - [Client.select_workspace_id](#clientselect_workspace_id)
- [Data Query Functions](#data-query-functions)
  - [Common Query Parameters](#common-query-parameters)
    - [Asset Selection Object](#asset-selection-object)
  - [Cycle Data](#cycle-data)
    - [Client.get_cycles](#clientget_cycles)
  - [Parts](#parts)
    - [Client.get_part_type_names](#clientget_part_type_names)
    - [Client.get_part_schema](#clientget_part_schema)
    - [Client.get_parts](#clientget_parts)
  - [Downtimes](#downtimes)
    - [Client.get_downtimes](#clientget_downtimes)
  - [KPIs](#kpis)
    - [Client.get_kpis](#clientget_kpis)
    - [Client.get_kpis_for_asset](#clientget_kpis_for_asset)
    - [Client.get_kpi_data_viz](#clientget_kpi_data_viz)
    - [Data Viz Query Object](#data-viz-query-object)
  - [Lines](#lines)
    - [Client.get_line_data](#clientget_line_data)
    - [Client.get_line_data_lineviz](#clientget_line_data_lineviz)
  - [Raw Data](#raw-data)
    - [Client.get_raw_data](#clientget_raw_data)
  - [Cookbooks](#cookbooks)
    - [Client.get_cookbooks](#clientget_cookbooks)
    - [Client.get_cookbook_top_results](#clientget_cookbook_top_results)
    - [Client.get_cookbook_current_value](#clientget_cookbook_current_value)
    - [Client.normalize_constraints](#clientnormalize_constraints)
    - [Cookbook Object Structure](#cookbook-object-structure)
    - [Recipe Run Object Structure](#recipe-run-object-structure)




## Instantiate Client

To interact with Sight Machine data, you first need to instantiate a client. This client handles the connection to the Sight Machine API.

The first step is to import the client submodule from the smsdk package. See the main [README.md](../README.md#installation) for installation instructions.

```python
from smsdk import client
```

Next, create an instance of the Client class. The 'tenant' argument should be set to the part of the tenant URL that preceeds '.sightmachine.io'. 

```python
tenant = 'demo'
cli = client.Client(tenant)
```

Finally, provide your API key and secret to initialize the connection. See [README.md -> Authenticating](../README.md#authenticating) for instructions for generating an API key and secret in-platform. The login function will return a boolean value indicating if the connection was successful. If it returns false, a few possible causes are invalid tenant name, incorrect API key and secret for that tenant, or lack of internet connection.

```python
success = cli.login('apikey', 
          key_id = api_key, 
          secret_id = api_secret)
if not success:
    raise AssertionError("SDK login failed.")
```





## General Metadata Functions

Functions in this section are for pulling general factory metadata.


### Machine Type Info
---


#### Client.get_machine_types

Get a list of tags available for each machine type and associated metadata for each tag.  Note that this includes extensive internal metadata.  If you only want to get a list of available machine types, see get_machine_type_names().

```python
cli.get_machine_types(source_type=None, source_type_clean=None)
```

Parameters:
> - **source_type**: *str, default None*
>   - Machine source_type to filter the output to. Note that this is a a Sight Machine internal machine type, not a UI-based display name.
> - **source_type_clean**: *str, default None*
>   - Machine source_type_clean to filter the output to. Note that this is a UI-based display name, not a Sight Machine internal machine type.

Returns:
> - **Pandas DataFrame**
>   - A table with full metadata about each machine type. 25 columns total.

Examples:

*Note that these examples are truncated because the output table is too large to display clearly.*


See all tag info
```python
>>> df = cli.get_machine_types()
>>> df.shape
(2439, 25)
```

Filter to one machine type
```python
>>> df = cli.get_machine_types(source_type_clean="Oven")
>>> df.shape
(142, 25)
```



#### Client.get_machine_type_names

Get a list of machine type names.

```python
cli.get_machine_type_names(clean_strings_out=True)
```

Parameters:
> - **clean_strings_out**: *boolean, default True*
>   - If true, return the list using the UI-based display names.  If false, the list contains the Sight Machine internal machine types.

Returns:
> - **list**
>   - A list of machine types.

Examples:


Machine type display names
```python
>>> cli.get_machine_type_names()
["Oven", "Fryer"]
```

Machine type internal names
```python
>>> cli.get_machine_type_names(clean_strings_out=False)
["mt_oven", "mt_fryer"]
```



#### Client.get_fields_of_machine_type

Get the available fields and field metadata for a specific machine type. This is similar to get_machine_schema(), but takes a machine type name directly instead of a machine name. Returns a list of dictionaries rather than a DataFrame.

```python
cli.get_fields_of_machine_type(machine_type=None, types=[], show_hidden=False)
```

Parameters:
> - **machine_type**: *str, required*
>   - The Sight Machine internal machine type name to get fields for.
> - **types**: *list, default []*
>   - A list of data type strings to filter by. If provided, only fields matching one of the specified types will be returned. Common types include "float", "int", "string", "boolean", "datetime".
> - **show_hidden**: *boolean, default False*
>   - If true, include fields that are hidden from the UI. By default, UI-hidden fields are excluded.

Returns:
> - **list**
>   - A list of dictionaries, each representing a field. Each dictionary includes keys such as `display_name`, `name`, `type`, `data_type`, `unit`, `stream_types`, and `raw_data_field`.

Examples:

Get all fields for a machine type
```python
>>> fields = cli.get_fields_of_machine_type("Lasercut")
>>> len(fields)
142
>>> fields[0]
{'display_name': 'Machine', 'unit': '', 'type': 'categorical', 'data_type': 'string', 'stream_types': [], 'raw_data_field': '', 'name': 'machine__source'}
```

Filter to only numeric fields
```python
>>> fields = cli.get_fields_of_machine_type("Lasercut", types=["float", "int"])
>>> len(fields)
98
```

Include hidden fields
```python
>>> fields = cli.get_fields_of_machine_type("Lasercut", show_hidden=True)
>>> len(fields)
155
```




### Machine Info
---




#### Client.get_machines

Get a list of all machines and their metadata. Notable metadata items are machine UI-based display name, Sight Machine internal name, machine type, and factory location. If you only want to get a list of available machines, see get_machine_names().

```python
cli.get_machines()
```

Returns:
> - **Pandas DataFrame**
>   - A table with metadata about each machine. There are 10 total columns.

Examples:

*Note that this example is truncated because the output table is too large to display clearly.*

Get all machines
```python
>>> df = cli.get_machines()
>>> df.shape
(20, 10)
```




#### Client.get_machine_names

Get a list of machine names.

```python
cli.get_machine_names(source_type=None, clean_strings_out=True)
```

Parameters:
> - **source_type**: *str, default None*
>   - Machine type to filter the output to. This accepts either a UI-based display name (e.g. "Oven") or a Sight Machine internal machine type (e.g. "mt_oven"). The function will first look for an exact internal name match and fall back to a display name lookup.
> - **clean_strings_out**: *boolean, default True*
>   - If true, return the list using the UI-based display names. If false, the list contains the Sight Machine internal machine names.

Returns:
> - **list**
>   - A list of machine names.

Examples:

Machine display names
```python
>>> cli.get_machine_names()
["Oven_1", "Fryer_2"]
```

Machine internal names
```python
>>> cli.get_machine_names(clean_strings_out=False)
["mt_oven_1", "mt_fryer_2"]
```

Filter by machine type (display name)
```python
>>> cli.get_machine_names(source_type="Oven")
["Oven_1", "Oven_2"]
```

Filter by machine type (internal name)
```python
>>> cli.get_machine_names(source_type="mt_oven")
["Oven_1", "Oven_2"]
```







#### Client.get_machine_schema

Get a table of available tags and tag metadata for a particular machine. Notable metadata items include Sight Machine internal name, display name, and data type. 

```python
cli.get_machine_schema(machine_source=None, types=[], show_hidden=False, return_mtype=False)
```

Parameters:
> - **machine_source**: *str, required*
>   - UI-based display name of the machine of interest.
> - **types**: *list, default []*
>   - A list of data type strings to filter by. If provided, only fields matching one of the specified types will be returned. Common types include "float", "int", "string", "boolean", "datetime".
> - **show_hidden**: *boolean, default False*
>   - If true, include fields that are hidden from the UI. By default, UI-hidden fields are excluded.
> - **return_mtype**: *boolean, default False*
>   - If true, return a tuple of (machine_type, DataFrame) instead of just the DataFrame. The machine_type is the internal Sight Machine machine type string.

Returns:
> - **Pandas DataFrame** (default)
>   - A table with metadata about each tag available for this machine. Columns include `display`, `name`, `sight_type`, and `type`.
> - **tuple** (if return_mtype=True)
>   - A tuple of (machine_type_string, DataFrame).


Examples:

*Note that this example is truncated because the output table is too large to display clearly.*

Get all tags for a machine
```python
>>> df = cli.get_machine_schema("Blender_1")
>>> df.shape
(158, 15)
```

Filter to numeric fields only
```python
>>> df = cli.get_machine_schema("Blender_1", types=["float"])
>>> df.shape
(120, 15)
```

Also return the machine type
```python
>>> machine_type, df = cli.get_machine_schema("Blender_1", return_mtype=True)
>>> machine_type
'mt_blender'
```



#### Client.get_type_from_machine

Given a machine's UI-based display name, get the Sight Machine internal machine type.

```python
cli.get_type_from_machine(machine_source=None)
```

Parameters:
> - **machine_source**: *str, required*
>   - UI-based display name of the machine of interest.

Returns:
> - **str**
>   - The associated machine type. Note that this is a Sight Machine internal machine type, not a UI-based display name.

Examples:

```python
>>> cli.get_type_from_machine("Oven_1")
"mt_oven"
```




### Other
---

#### Client.get_lines

Get information about the lines configured for this tenant. Data returned is in a JSON-like structure.

```python
cli.get_lines()
```

Returns:
> - **list**
>   - A list of dictionaries, each of which corresponds to a configured line. The dictionary contains line metadata and an ordered list of machines in that line.


Examples:

```python
>>> cli.get_lines()
[{'id': 'line-401a19b5',
  'factory_id': 'sanfrancisco',
  'display_name': 'Line 1',
  'display_order': [],
  'name': 'line-401a19b5',
  'order': 1,
  'machine': [
    {'name': 'Fryer_1', 'id': '1e4436e46df20d049faada54'},
    {'name': 'Oven_1', 'id': '7cd9277327457e26fa4deac2'}]
}]
```




#### Client.get_machine_timezone

Get the timezone that a machine is in. Timezone format is consistent with the [IANA Time Zone Database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) naming convention and is also compatible with the [pytz package](https://pypi.org/project/pytz/).

```python
cli.get_machine_timezone(machine_source=None)
```

Parameters:
> - **machine_source**: *str, required*
>   - UI-based display name of the machine of interest.

Returns:
> - **str**
>   - The timezone of the specified machine.

Examples:

```python
>>> cli.get_machine_timezone("Oven_1")
'America/Los_Angeles'
```




#### Client.create_share_link

Create a sharelink for a specific static Data Visualization chart. The link opens directly into the Data Visualization page with the specified chart pre-configured. **Note that a link will be generated even if the input values are invalid -- always verify the link works before sharing.**

```python
cli.create_share_link(
    assets=None, 
    chartType=None, 
    yAxis=None, 
    xAxis=X_AXIS_TIME,
    model="cycle", 
    time_selection=ONE_WEEK_RELATIVE,
    **kwargs
)
```

Parameters:
> - **assets**: *list, required*
>   - A list of machine display names (UI-based) to include in the chart. For cycle and KPI models, these are machine names like `["Oven_1", "Oven_2"]`. For line models, this can either be a list of machine names or a dict with `"assets"` and optional `"assetOffsets"` keys.
> - **chartType**: *str, required*
>   - The type of chart to render. Options are `"line"`, `"bar"`, `"scatter"`, and `"box"`.
> - **yAxis**: *dict, str, or list*
>   - The variable(s) to display on the y-axis. The format depends on the model:
>     - **For cycle model**: A dict describing the y-axis field from the Data Visualization API. The field should be a Sight Machine internal tag name.
>     - **For KPI model**: A list of KPI names (strings).
>     - **For line model**: A dict or list of dicts, each with keys `"field"` (internal tag name), `"machineName"` (display name), and optionally `"machineType"` (will be auto-populated if omitted).
> - **xAxis**: *dict, default X_AXIS_TIME*
>   - The variable to display on the x-axis. The default value results in Cycle End Time on the x-axis. For most use cases, the default is appropriate. The default is: `{"unit": "", "type": "datetime", "data_type": "datetime", "stream_types": [], "raw_data_field": "", "id": "endtime", "title": "Time", "isEnabled": True}`
> - **model**: *str, default "cycle"*
>   - The Sight Machine data model to source data from. Options are `"cycle"`, `"kpi"`, and `"line"`.
> - **time_selection**: *dict, default ONE_WEEK_RELATIVE*
>   - The time range for the chart. Supports both relative and absolute time selections:
>     - **Relative**: `{"time_type": "relative", "relative_start": 1, "relative_unit": "week", "ctime_tz": "America/Los_Angeles"}`
>     - **Absolute**: `{"time_type": "absolute", "start_time": "2024-11-01T00:00:00", "end_time": "2024-11-08T00:00:00", "time_zone": "America/Los_Angeles"}`
> - **resolution**: *str, default None*
>   - The time resolution for the chart. Options are `"second"`, `"minute"`, `"hour"`, `"day"`, `"week"`, `"month"`, and `"year"`. If None, Data Visualization will automatically choose an appropriate resolution.
> - **compareByField**: *str, default None*
>   - A tag to color/group results by. Must be a Sight Machine internal tag name, not a UI-based display name.


Returns:
> - **str**
>   - A URL string that links directly to the specified chart in Data Visualization.

Examples:

Create a share link for a cycle line chart over the last week
```python
>>> link = cli.create_share_link(
...     assets=["Oven_1"],
...     chartType="line",
...     yAxis={"id": "stats__Temperature__val", "title": "Temperature"},
...     model="cycle"
... )
>>> print(link)
'https://demo.sightmachine.io/#/analysis/datavis/s/a1b2c3d4'
```

Create a share link with an absolute time range
```python
>>> link = cli.create_share_link(
...     assets=["Oven_1", "Oven_2"],
...     chartType="scatter",
...     yAxis={"id": "stats__Pressure__val", "title": "Pressure"},
...     model="cycle",
...     time_selection={
...         "time_type": "absolute",
...         "start_time": "2024-11-01T00:00:00",
...         "end_time": "2024-11-08T00:00:00",
...         "time_zone": "America/Los_Angeles"
...     }
... )
```

Create a share link for a KPI chart
```python
>>> link = cli.create_share_link(
...     assets=["Oven_1"],
...     chartType="bar",
...     yAxis=["quality", "oee"],
...     model="kpi",
...     resolution="day"
... )
```

Create a share link for a line model chart
```python
>>> link = cli.create_share_link(
...     assets=["Oven_1", "Fryer_1"],
...     chartType="line",
...     yAxis=[
...         {"field": "stats__Temperature__val", "machineName": "Oven_1"},
...         {"field": "stats__OilTemp__val", "machineName": "Fryer_1"}
...     ],
...     model="line"
... )
```



#### Client.select_workspace_id

Set the SDK to pull all data and metadata from a non-production workspace. This setting applies to all future functions run with this client until otherwise specified. By default, the SDK pulls from the production workspace.

This is useful when working with development or staging pipelines that are not yet published to production.

```python
cli.select_workspace_id(workspace_id=None)
```

Parameters:
> - **workspace_id**: *str or int, required*
>   - The ID of the workspace to switch to. This can be found in the Sight Machine platform under pipeline settings.

Examples:

Switch to a development workspace
```python
>>> cli.select_workspace_id(workspace_id="ws-12345")
```

After calling this, all subsequent data queries will pull from the specified workspace rather than the production workspace.








## Data Query Functions

Functions in this section are for querying tabular data from the common Sight Machine data models: Cycles, Parts, Downtimes, KPIs, Lines, and Raw Data. There is also support for pulling information from Cookbooks.

Each data model must be configured on the tenant in order to query it. If a model is not set up for your tenant, the corresponding query function will return an error.

For detailed information about what each data model represents, see the [Sight Machine documentation](https://docs.sightmachine.com).


### Common Query Parameters

The data query functions for Cycles, Parts, and Downtimes share a common set of query parameters that control filtering, pagination, column selection, and sorting. These are passed as keyword arguments (`**kwargs`).

#### Filtering by Time

Time filters use the column name followed by a comparison operator suffix:

> - **End Time__gte**: *datetime* - End time greater than or equal to (i.e., records ending on or after this time)
> - **End Time__lte**: *datetime* - End time less than or equal to
> - **End Time__gt**: *datetime* - End time strictly greater than
> - **End Time__lt**: *datetime* - End time strictly less than
> - **Start Time__gte** / **Start Time__lte** / etc.: Same operators for start time

Time values should be Python `datetime` objects:
```python
from datetime import datetime

query = {
    'Machine': 'Oven_1',
    'End Time__gte': datetime(2024, 1, 1),
    'End Time__lte': datetime(2024, 1, 31)
}
```

#### Filtering by Value

Any tag or field can be filtered using operator suffixes:

> - **field\_\_in**: *list* - Value is in the provided list
> - **field\_\_nin**: *list* - Value is not in the provided list
> - **field\_\_ne**: *value* - Value is not equal to
> - **field\_\_exists**: *bool* - If True, only return records where the field is not null. If False, only return records where the field is null.
> - **field\_\_gte** / **field\_\_lte** / **field\_\_gt** / **field\_\_lt**: Numeric/date comparisons

```python
# Filter to specific machines
query = {'Machine__in': ['Oven_1', 'Oven_2'], ...}

# Exclude a product code
query = {'Product_Code__nin': ['ABC', 'DEF'], ...}

# Only records where a field exists
query = {'Defect_Reason__exists': True, ...}

# Numeric filter
query = {'output__ne': 0, ...}
```

#### Pagination and Selection

> - **_limit**: *int* - Maximum number of rows to return. If not specified, defaults to 5000 with a warning. Values over 5000 may lead to timeouts.
> - **_offset**: *int, default 0* - Number of rows to skip before returning results. Useful for paginating through large datasets.
> - **_only**: *list* - A list of column names to include in the output. If not specified, the first 50 fields are selected by default (with a warning). Set to `"*"` to select all fields (use with caution on wide tables).
> - **_order_by**: *str* - Column name to sort results by. Prefix with `-` for descending order.

```python
query = {
    'Machine': 'Oven_1',
    'End Time__gte': datetime(2024, 1, 1),
    'End Time__lte': datetime(2024, 1, 31),
    '_only': ['Machine', 'End Time', 'Temperature', 'Pressure'],
    '_limit': 1000,
    '_offset': 0,
    '_order_by': '-End Time'
}
```

#### String Cleaning Parameters

These parameters are available on get_cycles, get_parts, and get_downtimes:

> - **normalize**: *boolean, default True* - If true, flatten nested data structures in the response into a flat DataFrame.
> - **clean_strings_in**: *boolean, default True* - If true, the function will automatically convert UI-based display names in your query parameters into Sight Machine internal database names before sending the request.
> - **clean_strings_out**: *boolean, default True* - If true, the function will convert Sight Machine internal database column names in the returned DataFrame into UI-based display names.

In most cases, you should leave these at their defaults. This means you can use display names (like `"Temperature"`) in your queries and the returned DataFrame will also have display name columns. If you need to work with internal names (like `"stats__Temperature__val"`), set both to False.


#### Asset Selection Object

Several functions (`get_kpis_for_asset`, `get_kpi_data_viz`, line functions) take an `asset_selection` dict that tells the API which machines or machine types to operate on.

Select one or more machine types:
```python
asset_selection = {
    "machine_type": ["Lasercut"]
}
```

Select specific machines within a machine type:
```python
asset_selection = {
    "machine_type": ["Lasercut"],
    "machine_source": ["JB_AB_Lasercut_1"]
}
```

Both fields accept lists. For KPI-related functions, `machine_type` can be given as either the internal name (`"Lasercut"`) or the UI display name (`"Laser Cutter"`) — the SDK will translate automatically. For maximum safety, use the internal name returned by `get_type_from_machine()`.



### Cycle Data


#### Client.get_cycles

Retrieve cycle (machine) data. Each row represents one production cycle on a machine. The available columns are the tags configured for that machine type on the Sight Machine platform.

A machine must be specified in the query. If `_only` is not provided, the first 50 fields are selected by default. If `_limit` is not provided, it defaults to 5000.

```python
cli.get_cycles(**query)
```

Parameters:
> - **Machine**: *str, required*
>   - The machine display name to query data for. Can also be specified as `machine__source` (internal name). To query multiple machines, use `Machine__in` with a list.
> - All [common query parameters](#common-query-parameters) are supported.
> - **normalize**: *boolean, default True*
> - **clean_strings_in**: *boolean, default True*
> - **clean_strings_out**: *boolean, default True*

Returns:
> - **Pandas DataFrame**
>   - A table of cycle records. Datetime columns (`endtime`, `starttime`) are automatically converted to pandas Timestamp types.

Examples:

Basic cycle query
```python
from datetime import datetime

query = {
    'Machine': 'Oven_1',
    'End Time__gte': datetime(2024, 1, 1),
    'End Time__lte': datetime(2024, 1, 31),
    '_order_by': '-End Time',
    '_limit': 1000
}
df = cli.get_cycles(**query)
```

Select specific columns
```python
query = {
    'Machine': 'Oven_1',
    'End Time__gte': datetime(2024, 1, 1),
    'End Time__lte': datetime(2024, 1, 7),
    '_only': ['Machine', 'End Time', 'Temperature', 'Pressure', 'Output'],
    '_limit': 5000,
    '_order_by': '-End Time'
}
df = cli.get_cycles(**query)
```

Query multiple machines
```python
query = {
    'Machine__in': ['Oven_1', 'Oven_2'],
    'End Time__gte': datetime(2024, 1, 1),
    'End Time__lte': datetime(2024, 1, 7),
    '_only': ['Machine', 'End Time', 'Temperature'],
    '_limit': 5000
}
df = cli.get_cycles(**query)
```

Filter by a tag value
```python
query = {
    'Machine': 'Oven_1',
    'End Time__gte': datetime(2024, 1, 1),
    'End Time__lte': datetime(2024, 1, 31),
    'output__ne': 0,
    '_only': ['Machine', 'End Time', 'Output', 'Temperature'],
    '_limit': 5000
}
df = cli.get_cycles(**query)
```


### Parts

#### Client.get_part_type_names

Get a list of available part type names on this tenant.

```python
cli.get_part_type_names(clean_strings_out=True)
```

Parameters:
> - **clean_strings_out**: *boolean, default True*
>   - If true, return the list using UI-based display names. If false, the list contains Sight Machine internal part type names.

Returns:
> - **list**
>   - A list of part type name strings.

Examples:

```python
>>> cli.get_part_type_names()
["Engine Block", "Transmission Housing"]
```

```python
>>> cli.get_part_type_names(clean_strings_out=False)
["engine_block", "transmission_housing"]
```


#### Client.get_part_schema

Get a table of available fields and field metadata for a particular part type.

```python
cli.get_part_schema(part_type, types=[])
```

Parameters:
> - **part_type**: *str, required*
>   - The part type to get the schema for. Accepts either a display name or internal name.
> - **types**: *list, default []*
>   - A list of data type strings to filter by (e.g., `["float", "string"]`). If empty, all fields are returned.

Returns:
> - **Pandas DataFrame**
>   - A table with columns `name`, `display`, and `type` describing each available field.

Examples:

```python
>>> schema = cli.get_part_schema("Engine Block")
>>> schema.shape
(85, 3)
>>> schema.head()
                         name          display     type
0  stats__Weight__val          Weight          float
1  stats__Length__val          Length          float
```


#### Client.get_parts

Retrieve part data. Each row represents one part record. Parts aggregate data across multiple machines and represent a finished or in-progress product.

A part type must be specified in the query. If `_only` is not provided, the first 50 fields are selected by default along with standard top-level fields (part type, serial, timestamps, state). If `_limit` is not provided, it defaults to 5000.

```python
cli.get_parts(**query)
```

Parameters:
> - **Part**: *str, required*
>   - The part type display name to query. Can also be specified as `type__part_type` (internal name). To query multiple part types, use `Part__in` with a list.
> - All [common query parameters](#common-query-parameters) are supported.
> - **normalize**: *boolean, default True*
> - **clean_strings_in**: *boolean, default True*
> - **clean_strings_out**: *boolean, default True*

Returns:
> - **Pandas DataFrame**
>   - A table of part records. Datetime columns are automatically converted to pandas Timestamp types.

Examples:

Basic part query
```python
from datetime import datetime

query = {
    'Part': 'Engine Block',
    'End Time__gte': datetime(2024, 1, 1),
    'End Time__lte': datetime(2024, 1, 31),
    '_order_by': '-End Time',
    '_limit': 1000
}
df = cli.get_parts(**query)
```

Select specific columns and filter
```python
query = {
    'Part': 'Engine Block',
    'End Time__gte': datetime(2024, 1, 1),
    'End Time__lte': datetime(2024, 1, 31),
    'Defect_Reason__exists': True,
    '_limit': 500,
    '_only': ['Part', 'End Time', 'Serial', 'State (Pass / Fail)', 'Weight']
}
df = cli.get_parts(**query)
```


### Downtimes

#### Client.get_downtimes

Retrieve downtime data. Each row represents one downtime event for a machine.

A machine must be specified in the query. If `_only` is not provided, the default downtime fields are selected: Machine, Start Time, End Time, Duration, Shift, Downtime Reason, Downtime Category, and Downtime Type. If `_limit` is not provided, it defaults to 5000.

```python
cli.get_downtimes(**query)
```

Parameters:
> - **Machine**: *str, required*
>   - The machine display name to query downtime data for. Can also be specified as `machine__source`. To query multiple machines, use `Machine__in` with a list.
> - All [common query parameters](#common-query-parameters) are supported.
> - **normalize**: *boolean, default True*
> - **clean_strings_in**: *boolean, default True*
> - **clean_strings_out**: *boolean, default True*

Returns:
> - **Pandas DataFrame**
>   - A table of downtime records. Datetime columns are automatically converted to pandas Timestamp types.

Examples:

Basic downtime query
```python
from datetime import datetime

query = {
    'Machine': 'Oven_1',
    'End Time__gte': datetime(2024, 1, 1),
    'End Time__lte': datetime(2024, 1, 31),
    '_order_by': '-End Time',
    '_limit': 1000
}
df = cli.get_downtimes(**query)
```

Select specific columns
```python
query = {
    'Machine': 'Oven_1',
    'End Time__gte': datetime(2024, 1, 1),
    'End Time__lte': datetime(2024, 1, 31),
    '_only': ['Machine', 'Start Time', 'End Time', 'Duration', 'Downtime Reason'],
    '_order_by': '-End Time'
}
df = cli.get_downtimes(**query)
```


### KPIs

#### Client.get_kpis

Get a list of all KPIs configured for this tenant.

```python
cli.get_kpis()
```

Returns:
> - **list**
>   - A list of dictionaries, each describing an available KPI. Each dictionary includes keys like `name` and `display_name`.

Examples:

```python
>>> kpis = cli.get_kpis()
>>> for kpi in kpis[:3]:
...     print(kpi['name'], '-', kpi.get('display_name', ''))
quality - Quality
oee - OEE
availability - Availability
```


#### Client.get_kpis_for_asset

Get the list of KPIs available for a specific asset (machine type and/or machine).

```python
cli.get_kpis_for_asset(asset_selection=None)
```

Parameters:
> - **asset_selection**: *dict, required*
>   - A dictionary specifying the asset to get KPIs for. This should have a `machine_type` key and optionally a `machine_source` key. Both display names and internal names are accepted -- display names will be automatically converted.
>   - Format: `{"machine_type": ["MachineTypeName"], "machine_source": ["MachineName"]}`

Returns:
> - **list**
>   - A list of dictionaries describing the available KPIs for the specified asset.

Examples:

Get KPIs for a machine type
```python
>>> kpis = cli.get_kpis_for_asset(
...     asset_selection={
...         'machine_type': ['Oven'],
...         'machine_source': ['Oven_1']
...     }
... )
>>> [kpi['name'] for kpi in kpis[:3]]
['quality', 'oee', 'availability']
```


#### Client.get_kpi_data_viz

Retrieve KPI data via the Data Visualization API. This function returns aggregated KPI values over time or grouped by independent variables.

```python
cli.get_kpi_data_viz(
    machine_sources=None, 
    kpis=None, 
    i_vars=None, 
    time_selection=None, 
    **kwargs
)
```

Parameters:
> - **machine_sources**: *list, default None*
>   - A list of machine display names to query KPI data for. The function automatically resolves machine types from the machine names.
> - **kpis**: *list, default None*
>   - A list of KPI name strings to retrieve (e.g., `["quality", "oee"]`). Each KPI is queried with the `"avg"` aggregation by default.
> - **i_vars**: *list, default None*
>   - A list of independent variable dictionaries for grouping/bucketing the data. See the [Data Viz Query Object](#data-viz-query-object) section below for the full i_vars format.
>   - Common example: `[{"name": "endtime", "time_resolution": "day", "query_tz": "America/Los_Angeles", "output_tz": "America/Los_Angeles"}]`
> - **time_selection**: *dict, default None*
>   - The time range for the query. Supports both relative and absolute formats. See the [Data Viz Query Object](#data-viz-query-object) section below for details.

You can also pass the full Data Viz query structure directly as keyword arguments. See the [Data Viz Query Object](#data-viz-query-object) section below for the complete query format.

Returns:
> - **list**
>   - A list of data points. Each data point is a dictionary with `i_vals` (independent variable values including time bins) and `d_vals` (dependent variable/KPI values with aggregations).

Examples:

Get daily KPI values for the last week
```python
data = cli.get_kpi_data_viz(
    machine_sources=['Oven_1'],
    kpis=['quality', 'oee'],
    i_vars=[{
        'name': 'endtime',
        'time_resolution': 'day',
        'query_tz': 'America/Los_Angeles',
        'output_tz': 'America/Los_Angeles'
    }],
    time_selection={
        'time_type': 'relative',
        'relative_start': 1,
        'relative_unit': 'week',
        'ctime_tz': 'America/Los_Angeles'
    }
)
```

The returned data has the following structure:
```python
[
    {
        "i_vals": {
            "endtime": {"bin_min": "2024-01-01", "bin_avg": "2024-01-01T12:00:00"}
        },
        "d_vals": {
            "quality": {"avg": 0.95},
            "oee": {"avg": 0.87}
        }
    },
    ...
]
```


#### Data Viz Query Object

`get_kpi_data_viz` and the Lines data-viz functions accept additional Data Viz query fields as keyword arguments. A complete Data Viz query has this shape:

```python
{
    "asset_selection": {
        "machine_source": ["JB_AB_Lasercut_1"],
        "machine_type": ["Lasercut"]
    },
    "d_vars": [
        {"name": "quality", "aggregate": ["avg"]}
    ],
    "i_vars": [
        {
            "name": "endtime",
            "time_resolution": "day",
            "query_tz": "America/Los_Angeles",
            "output_tz": "America/Los_Angeles",
            "bin_strategy": "user_defined2",
            "bin_count": 50
        }
    ],
    "time_selection": {
        "time_type": "relative",
        "relative_start": 7,
        "relative_unit": "year",
        "ctime_tz": "America/Los_Angeles"
    },
    "where": [],
    "db_mode": "sql"
}
```

##### asset_selection
See [Asset Selection Object](#asset-selection-object).

##### d_vars — dependent variables
A list of fields to return, each with an aggregate. The SDK builds this automatically from `get_kpi_data_viz`'s `kpis` argument but you can override it.

> - **name**: *str* — name of the dependent variable (KPI name or tag name)
> - **aggregate**: *list* — aggregation(s) to apply. Supported: `avg`, `sum`, `min`, `max`.

##### i_vars — independent variables
Typically a single time-based variable describing how to bin results along the x-axis.

> - **name**: *str* — typically `"endtime"`
> - **time_resolution**: *str, optional* — one of `year`, `quarter`, `month`, `week`, `day`, `hour`, `minute`, `second`
> - **query_tz**: *str, optional* — time zone the query is interpreted in
> - **output_tz**: *str, optional* — time zone the returned timestamps are expressed in
> - **bin_strategy**: *str, optional* — one of `user_defined2`, `none`, `categorical`
> - **bin_count**: *int, optional* — number of bins to split the data into

##### time_selection
Defines the time window for the query. Two shapes supported.

Relative (go back N units from now):
```python
{
    "time_type": "relative",
    "relative_start": 7,
    "relative_unit": "year",
    "ctime_tz": "America/Los_Angeles"
}
```
- **time_type**: `"relative"`
- **relative_start**: *int* — how many units back
- **relative_unit**: *str* — one of `year`, `month`, `week`, `day`, `hour`, `minute`, `second`
- **ctime_tz**: *str* — time zone

Absolute (fixed window):
```python
{
    "time_type": "absolute",
    "start_time": "2023-02-23T08:00:00.000Z",
    "end_time": "2023-03-01T21:35:35.499Z",
    "time_zone": "America/Los_Angeles"
}
```
- **time_type**: `"absolute"`
- **start_time** / **end_time**: ISO-8601 timestamps
- **time_zone**: *str*

##### where — record filters (optional)
A list of filter clauses that are AND-ed together:
```python
{"name": "type__part_type", "op": "eq", "value": "EngineBlock"}
```

> - **name**: *str* — the field to filter on
> - **op**: *str* — the comparison operator (e.g., `eq`, `ne`, `gt`, `gte`, `lt`, `lte`)
> - **value**: any — the value to compare against

##### db_mode (optional)
Defaults to `"sql"`. A `"mongo"` mode exists but should rarely be needed.



### Lines

Line functions query data from the Lines data model, which combines data from multiple machines in a production line into a single unified view.

Note: the get_lines() function listed in the [General Metadata Functions](#clientget_lines) section returns line configuration metadata. The functions below query actual line production data.


#### Client.get_line_data

Retrieve tabular line data. This queries the line data model and returns a flat table similar to cycle data, but spanning multiple machines in a line.

```python
cli.get_line_data(
    assets=None,
    fields=[],
    time_selection=ONE_DAY_RELATIVE,
    asset_time_offset={},
    filters=[],
    limit=400,
    offset=0
)
```

Parameters:
> - **assets**: *list, required*
>   - A list of machine display names that belong to the line you want to query.
> - **fields**: *list, default []*
>   - A list of field selection dictionaries specifying which fields to return. Each dictionary should have `"asset"` and `"name"` keys. Example: `[{"asset": "Oven_1", "name": "Temperature"}]`. If empty, default fields are returned.
> - **time_selection**: *dict, default ONE_DAY_RELATIVE*
>   - The time range for the query. Supports both relative and absolute formats. Default is the last 24 hours relative. See [Data Viz Query Object](#data-viz-query-object) for details on the format.
> - **asset_time_offset**: *dict, default {}*
>   - A dictionary mapping machine names to their time offsets within the line. Each offset is a dict with `"interval"` (number) and `"period"` (unit string, e.g. `"minutes"`). If not specified for a machine, defaults to `{"interval": 0, "period": "minutes"}`.
> - **filters**: *list, default []*
>   - A list of filter conditions to narrow results. Each filter follows the where clause format described in the [Data Viz Query Object](#data-viz-query-object).
> - **limit**: *int, default 400*
>   - Maximum number of rows to return.
> - **offset**: *int, default 0*
>   - Number of rows to skip for pagination.

Returns:
> - **list**
>   - A list of records (dictionaries) containing the requested line data.

Examples:

Get line data for two machines over the last day
```python
data = cli.get_line_data(
    assets=['Oven_1', 'Fryer_1'],
    fields=[
        {'asset': 'Oven_1', 'name': 'Temperature'},
        {'asset': 'Fryer_1', 'name': 'Oil_Temperature'}
    ],
    time_selection={
        'time_type': 'relative',
        'relative_start': 1,
        'relative_unit': 'day',
        'ctime_tz': 'America/Los_Angeles'
    },
    limit=400
)
```


#### Client.get_line_data_lineviz

Retrieve line data via the Line Visualization API. This is an async-based query that returns aggregated line data, similar to what is displayed in the Line Visualization page of the platform.

```python
cli.get_line_data_lineviz(
    assets=None,
    d_vars=None,
    i_vars=None,
    time_selection=ONE_DAY_RELATIVE,
    asset_time_offset={},
    filters=[]
)
```

Parameters:
> - **assets**: *list, default None*
>   - A list of machine display names in the line.
> - **d_vars**: *list, default None*
>   - A list of dependent variable dictionaries. See [Data Viz Query Object](#data-viz-query-object) for the d_vars format.
> - **i_vars**: *list, default None*
>   - A list of independent variable dictionaries. See [Data Viz Query Object](#data-viz-query-object) for the i_vars format.
> - **time_selection**: *dict, default ONE_DAY_RELATIVE*
>   - The time range for the query. Supports both relative and absolute formats.
> - **asset_time_offset**: *dict, default {}*
>   - Time offsets for each machine in the line.
> - **filters**: *list, default []*
>   - Filter conditions to narrow results.

Returns:
> - **list**
>   - Aggregated line visualization data.

Examples:

```python
data = cli.get_line_data_lineviz(
    assets=['Oven_1', 'Fryer_1'],
    d_vars=[
        {'name': 'stats__Temperature__val', 'aggregate': ['avg']}
    ],
    i_vars=[{
        'name': 'endtime',
        'time_resolution': 'hour'
    }],
    time_selection={
        'time_type': 'relative',
        'relative_start': 1,
        'relative_unit': 'day',
        'ctime_tz': 'America/Los_Angeles'
    }
)
```


### Raw Data

#### Client.get_raw_data

Retrieve raw sensor data. Raw data is the unprocessed data collected directly from equipment sensors, before it is aggregated into cycles. This data is typically at a much higher frequency than cycle data.

```python
cli.get_raw_data(
    raw_data_table=None,
    fields=[],
    time_selection=ONE_DAY_RELATIVE,
    limit=400,
    offset=0
)
```

Parameters:
> - **raw_data_table**: *str, required*
>   - The name of the raw data table to query. This corresponds to the raw data source configured on the platform.
> - **fields**: *list, default []*
>   - A list of field name strings to include in the results. Example: `["temperature", "pressure", "speed"]`. If empty, default fields are returned.
> - **time_selection**: *dict, default ONE_DAY_RELATIVE*
>   - The time range for the query. Default is the last 24 hours relative. Supports both relative and absolute formats. See [Data Viz Query Object](#data-viz-query-object) for details on the format.
> - **limit**: *int, default 400*
>   - Maximum number of rows to return.
> - **offset**: *int, default 0*
>   - Number of rows to skip for pagination.

Returns:
> - **Pandas DataFrame**
>   - A table of raw data records.

Examples:

Get raw data for the last day
```python
df = cli.get_raw_data(
    raw_data_table='oven_sensors',
    fields=['temperature', 'pressure', 'humidity'],
    time_selection={
        'time_type': 'relative',
        'relative_start': 1,
        'relative_unit': 'day',
        'ctime_tz': 'America/Los_Angeles'
    },
    limit=1000
)
```

Get raw data for a specific time range
```python
df = cli.get_raw_data(
    raw_data_table='oven_sensors',
    fields=['temperature'],
    time_selection={
        'time_type': 'absolute',
        'start_time': '2024-01-01T00:00:00',
        'end_time': '2024-01-01T06:00:00',
        'time_zone': 'America/Los_Angeles'
    },
    limit=5000,
    offset=0
)
```


### Cookbooks

Cookbook functions interact with the Sight Machine Cookbooks feature, which provides recipe optimization recommendations.


#### Client.get_cookbooks

Get a list of all cookbooks accessible to the logged-in user, including both deployed and undeployed cookbooks.

```python
cli.get_cookbooks()
```

Returns:
> - **list**
>   - A list of dictionaries, each representing a cookbook. Each dictionary contains metadata about the cookbook including its name, ID, recipe groups, and deployment status.

Examples:

```python
>>> cookbooks = cli.get_cookbooks()
>>> for cb in cookbooks:
...     print(cb['name'])
Oven Temperature Optimization
Fryer Oil Quality
```


#### Client.get_cookbook_top_results

Get the top-performing runs for a specific recipe group within a cookbook. A "run" represents a period of time where conditions matched a recipe's recommended settings.

```python
cli.get_cookbook_top_results(recipe_group_id=None, limit=10)
```

Parameters:
> - **recipe_group_id**: *str, required*
>   - The ID of the recipe group to get results for. This can be found in the cookbook metadata returned by get_cookbooks().
> - **limit**: *int, default 10*
>   - The maximum number of top runs to return.

Returns:
> - **dict**
>   - A dictionary with keys `"runs"` (a list of run records) and `"constraint_groups"` (the constraint definitions for the recipe).

Examples:

```python
>>> results = cli.get_cookbook_top_results(
...     recipe_group_id='rg-abc123',
...     limit=5
... )
>>> len(results['runs'])
5
>>> results['runs'][0].keys()
dict_keys(['start_time', 'end_time', 'score', ...])
```


#### Client.get_cookbook_current_value

Get the current (most recent) value of specific machine fields. This is useful for checking current conditions against cookbook recipe recommendations.

```python
cli.get_cookbook_current_value(variables=[], minutes=1440)
```

Parameters:
> - **variables**: *list, required*
>   - A list of dictionaries, each specifying a field to get the current value for. Each dictionary must have `"asset"` (machine name) and `"name"` (field name) keys.
> - **minutes**: *int, default 1440*
>   - The time window (in minutes) to look back when finding the most recent value. Default is 1440 minutes (24 hours).

Returns:
> - **list**
>   - A list of current values corresponding to the requested variables.

Examples:

```python
>>> values = cli.get_cookbook_current_value(
...     variables=[
...         {'asset': 'Oven_1', 'name': 'Temperature'},
...         {'asset': 'Oven_1', 'name': 'Pressure'}
...     ],
...     minutes=60
... )
>>> values
[{'asset': 'Oven_1', 'name': 'Temperature', 'value': 375.2},
 {'asset': 'Oven_1', 'name': 'Pressure', 'value': 14.7}]
```


#### Client.normalize_constraints

Convert a list of cookbook constraint range objects into human-readable string representations. This is a utility function for working with cookbook recipe constraints.

```python
cli.normalize_constraints(constraints)
```

Parameters:
> - **constraints**: *list, required*
>   - A list of constraint dictionaries. Each dictionary must have `"to"` and `"from"` keys specifying the range bounds, and optionally `"to_is_inclusive"` and `"from_is_inclusive"` boolean keys.

Returns:
> - **list**
>   - A list of strings representing each constraint range. Square brackets `[]` indicate inclusive bounds and parentheses `()` indicate exclusive bounds.

Examples:

```python
>>> constraints = [
...     {'to': 100, 'from': 200, 'to_is_inclusive': True, 'from_is_inclusive': True},
...     {'to': 50, 'from': None, 'to_is_inclusive': False, 'from_is_inclusive': False}
... ]
>>> cli.normalize_constraints(constraints)
['[100,200]', '(50,None)']
```


#### Cookbook Object Structure

`get_cookbooks()` returns a list of cookbook dicts. Each dict looks like this:

```python
{
    "hash": "...",
    "name": "Oven Temperature Optimization",
    "assetNames": ["JB_HM_Diecast_1"],
    "key_constraint": {
        "field": {
            "fieldName": "stats__Cylinders__val",
            "machineId": "e2df2b4f115b763f45d04fa2",
            "machineName": "JB_HM_Diecast_1",
            "machineDisplayName": "Hamilton - Diecast 1",
            "fieldType": "categorical",
            "machineType": "Diecast",
            "fieldDisplayName": "Cylinders",
            "fieldUnit": ""
        },
        "valueMap": {"4": 1, "6": 0}
    },
    "recipe_groups": [...],
    "metadata": {"created_by": {...}},
    "updatetime": "2023-03-16 17:48:55.355000",
    "assets": [],
    "id": "63ab6b263fa4880c06334b03"
}
```

Top-level fields:

> - **hash**: *str* — hash of the cookbook object
> - **name**: *str* — cookbook name
> - **assetNames**: *list* — machine names the cookbook runs against
> - **key_constraint**: *dict* — the field whose value determines which recipe group (product) is used. `valueMap` maps each value to a recipe-group index.
> - **recipe_groups**: *list* — one entry per product (see below)
> - **metadata**: *dict* — `created_by` info (user ID, email, name)
> - **updatetime**: *str* — last-updated timestamp
> - **assets**: *list* — list of assets used in the cookbook
> - **id**: *str* — cookbook ID

##### Recipe group

Each entry in `recipe_groups` represents one product within the cookbook:

```python
{
    "id": "rg-abc",
    "values": [1],
    "runBoundaries": [],
    "maxDuration": {"isEnabled": False, "minimum": 0, "unit": "second"},
    "topRun": 10,
    "constraints": [...],
    "levers": [...],
    "outcomes": [...],
    "filters": {"duration": {...}, "recordFilters": []},
    "dateRange": {"value": {...}, "config": {...}},
    "computeDeployedDateRange": None,
    "statsCalculationSetting": "default",
    "deployed": {...}
}
```

> - **id**: *str* — recipe-group ID (pass this to `get_cookbook_top_results`)
> - **values**: *list* — values currently in this group
> - **topRun**: *int* — number of top runs considered when computing lever stats
> - **constraints**: *list* — fields + value ranges used to partition runs
> - **levers**: *list* — fields that vary between recipes (the knobs)
> - **outcomes**: *list* — fields being optimized
> - **filters**: *dict* — duration threshold + record-level filters
> - **dateRange**: *dict* — time window considered when computing recipes
> - **deployed**: *dict* — the deployed version of this recipe group, minus this field
> - **runBoundaries**, **maxDuration**, **computeDeployedDateRange**, **statsCalculationSetting**: currently unused or legacy

##### Constraints (within a recipe group)

Each constraint defines the value ranges that delimit runs:

```python
{
    "asset": "F1_010_BodyMaker_4",
    "name": "stats__BM 001: Cans Out__val",
    "type": "continuous",
    "values": [
        {"from": None, "from_is_inclusive": False, "to": 340, "to_is_inclusive": False},
        {"from": 340, "from_is_inclusive": True, "to": 6000, "to_is_inclusive": True},
        {"from": 6000, "from_is_inclusive": False, "to": None, "to_is_inclusive": False}
    ]
}
```

> - **asset**: *str* — machine name the constraint field is on
> - **name**: *str* — internal field name
> - **type**: *str* — data type (typically `"continuous"` or `"categorical"`)
> - **values**: *list* — the value bands. Pass these to `normalize_constraints()` to get compact string labels.

##### Levers and outcomes

Both `levers` and `outcomes` entries use the same "field descriptor" shape:

```python
{
    "fieldName": "stats__AluminumTempAvg__val",
    "machineId": "e2df2b4f115b763f45d04fa2",
    "machineName": "JB_HM_Diecast_1",
    "machineDisplayName": "Hamilton - Diecast 1",
    "fieldType": "continuous",
    "machineType": "Diecast",
    "fieldDisplayName": "AluminumTemp - Average",
    "fieldUnit": "celsius"
}
```

Outcomes wrap that descriptor with optimization metadata:
```python
{
    "field": { ...descriptor as above... },
    "weight": 1,
    "optimization_func": "maximize"
}
```

> - **weight**: *number* — relative importance vs. other outcomes
> - **optimization_func**: *str* — typically `"maximize"` or `"minimize"`


#### Recipe Run Object Structure

`get_cookbook_top_results()` returns a dict with two views: `runs` (one entry per run) and `constraint_groups` (one entry per recipe, the aggregate view). An individual run looks like:

```python
{
    "_count": 12,
    "_count_muted": 0,
    "_duration_seconds": 649.0,
    "_earliest": "2022-10-21T00:35:32+00:00",
    "_latest": "2022-10-21T00:46:21+00:00",
    "_score": 1.0,
    "constraint_group_id": "0",
    "constraints": [...],
    "cookbook": "63ab6b263fa4880c06334b03",
    "filters": [],
    "i_vals": [
        {"asset": "SHARED", "name": "group", "value": "0"},
        {"asset": "SHARED", "name": "sequence", "value": 2}
    ],
    "levers": [...],
    "outcomes": [...]
}
```

Top-level fields:

> - **_count**: *int* — total records in the run
> - **_count_muted**: *int* — records filtered out
> - **_duration_seconds**: *float* — run duration in seconds
> - **_earliest** / **_latest**: *str* — ISO timestamps bounding the run
> - **_score**: *float* — the score this run achieved under the cookbook's weighting
> - **constraint_group_id**: *str* — which recipe group (product) the run belongs to
> - **constraints**: *list* — the constraint values the run fell into
> - **cookbook**: *str* — parent cookbook ID
> - **filters**: *list* — filters applied to the run
> - **i_vals**: *list* — constraint / run-boundary values used to delimit this run
> - **levers**: *list* — lever values during the run (see below)
> - **outcomes**: *list* — outcome values during the run (see below)

##### Lever entry
```python
{
    "asset": "JB_HM_Diecast_1",
    "d_pos": 2,
    "name": "stats__AluminumTempAvg__val",
    "value": {
        "avg": 659.84,
        "count": 9.0,
        "max": 671.10,
        "min": 653.72,
        "var_pop": 29.82
    }
}
```

> - **asset**: *str* — machine name
> - **d_pos**: *int* — index of the corresponding dependent variable (internal)
> - **name**: *str* — internal field name
> - **value**: *dict* — measurement stats: `avg`, `count`, `max`, `min`, `var_pop`

##### Outcome entry
```python
{
    "asset": "JB_HM_Diecast_1",
    "d_pos": 0,
    "kpi": {
        "aggregates": {"Output": "sum", "ScrapQuantity": "sum"},
        "dependencies": {"Output": 9.0, "ScrapQuantity": 0.0},
        "formula": "((Output) / (Output + ScrapQuantity)) * 100 if ((Output + ScrapQuantity) > 0) else None"
    },
    "name": "quality",
    "value": {
        "avg": 100.0,
        "count": 100.0,
        "max": 100.0,
        "min": 100.0,
        "normal": 1.0,
        "var_pop": 100.0
    }
}
```

> - **asset**, **d_pos**, **name**: as with levers
> - **kpi**: *dict, only present when the outcome is a KPI* — shows the KPI's formula, its input aggregations, and the dependency values during this run
> - **value**: *dict* — measurement stats including an additional **normal** field (measure of the distribution's normality)
