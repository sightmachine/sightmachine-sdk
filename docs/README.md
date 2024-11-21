# All Functions

This document provides an overview of the various functions available in the Sight Machine SDK. These functions are designed to help you interact with and retrieve data from the Sight Machine platform efficiently. Each function is accompanied by example code snippets to demonstrate their usage and to help you integrate them into your own applications. 

Functions are split into general functions which pull general factory metadata, and data queries which pull tabular data from the various data models. All functions are methods of the client object, which needs to be instantiated first.


TODO generate table of contents

TODO make sure I got all important functions

TODO make sure I have all the sections for each function

TODO describe what errors look like for each and what can cause them




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
>   - Machine source_type to filter the output to. Note that this is a Sight Machine internal machine type, not a UI-based display name.
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








#### Client.get_machine_schema

Get a table of available tags and tag metadata for a particular machine. Notable metadata items include Sight Machine internal name, display name, and data type. 

```python
cli.get_machine_schema(machine_source=None)
```

Parameters:
> - **machine_source**: *str, default None*
>   - UI-based display name of the machine of interest.

Returns:
> - **Pandas DataFrame**
>   - A table with metadata about each tag available for this machine. There are 15 total columns.


Examples:

*Note that this example is truncated because the output table is too large to display clearly.*

Get all machines
```python
>>> df = cli.get_machine_schema("Blender_1")
>>> df.shape
(158, 15)
```




#### Client.get_type_from_machine

Given a machine's UI-based display name, get the Sight Machine internal machine type.

```python
cli.get_type_from_machine(machine_source=None)
```

Parameters:
> - **machine_source**: *str, default None*
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
> - **machine_source**: *str, default None*
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

Create a sharelink for a specific static Data Vizualization chart. **Note that a link will be generated even if the input values are invalid.**

```python
cli.create_share_link(assets=None, chartType=None, yAxis=None, xAxis={"unit": "", "type": "datetime", "data_type": "datetime", "stream_types": [], "raw_data_field": "", "id": "endtime", "title": "Time", "isEnabled": True}, model="cycle", time_selection={"time_type": "relative", "relative_start": 1, "relative_unit": "week", "ctime_tz": "America/Los_Angeles"})
```

Parameters:
> - **assets**: *list, default None*
>   - A list of asset IDs to include in the share link.
TODO fix above, need internal asset names
> - **chartType**: *str, default None*
>   - The type of chart to create a share link for. Options are "line", "bar", "scatter", and "box".
> - **yAxis**: *str, default None*
>   - The variable to display on the y-axis of the chart.
TODO fix above, need internal tag names
> - **xAxis**: *str, default {"unit": "", "type": "datetime", "data_type": "datetime", "stream_types": [], "raw_data_field": "", "id": "endtime", "title": "Time", "isEnabled": True}*
>   - The variable to display on the x-axis of the chart. Default value results in Cycle End Time on the X-axis.
TODO more details about options, need internal tag names
> - **model**: *str, default "cycle"*
>   - The Sight Machine data model to use for source data. Options are 'cycle', 'kpi', and 'line'.
TODO make sure these are the correct options
> - **time_selection**: *str, default {"time_type": "relative", "relative_start": 1, "relative_unit": "week", "ctime_tz": "America/Los_Angeles"}*
>   - The time range for the data to be displayed in the chart. Default value renders the last week of data. The default value is a relative selection. You can also do an absolute time selection with the following format: time_selection = {"time_type": "absolute" "start_time": "2024-11-11T00:00:00", "end_time": "2024-11-10T00:00:00", "time_zone": "America/Los_Angeles"}. If an absolute time range is chosen, start and end time must be in ISO format.
> - **resolution**: *str, default None*
>   - The time resolution that the chart should be in. Options are 'second', 'minute', 'hour', 'week', 'month', and 'year'. If None is chosen, Data Vizualization will logically choose one for you.
> - **compareByField**: *str, default None*
>   - The tag to color results based on. The tag name needs to be a Sight Machine internal tag name, not a UI-based display name.


Returns:
> - **str**
>   - A URL string that can be used to share the specified chart.

Examples:

TODO fix examples 

Create a share link for a cycle chart
```python
>>> share_link = cli.create_share_link(assets=['asset_1'], chartType='line', yAxis='Temperature', xAxis='Time', model='cycle', time_selection='ONE_WEEK_RELATIVE')
>>> print(share_link)
'https://demo.sightmachine.io/#/analysis/datavis/s/123456'
```

Create a share link for a downtime chart
```python
>>> share_link = cli.create_share_link(assets=['asset_2'], chartType='bar', yAxis='Downtime', xAxis='Time', model='downtime', time_selection='ONE_DAY_RELATIVE')
>>> print(share_link)
'https://demo.sightmachine.io/#/analysis/datavis/s/123456'
```







#### Client.select_workspace_id

Set the SMSDK to pull all data and metadata from a non-production workspace. This setting applies to all future functions run with this client until otherwise specified.


```python
cli.select_workspace_id(workspace_id=None)
```














## Data Query Functions

Functions in this section are for querying tabular data from our common data models: Cycles, Parts, Downtimes, KPI, Lines, and Raw Data. We also have support for pulling information from Cookbooks.

TODO reference Sight Machine docs for info on these models?
TODO mention that it only works if the model is setup? what happens if the model isn't set up?


### Cycle Data


```python
query = {'Machine': machines[0],
         'End Time__gte' : datetime(2023, 4, 1), 
         'End Time__lte' : datetime(2023, 4, 2), 
         '_order_by': '-End Time'}
TODO include other options in query 
df = cli.get_cycles(**query)
```

### Parts
```python
cli.get_part_type_names()
cli.get_part_schema(part_type)
```

```python
query = {'Part': part_type,
         'End Time__gte' : datetime(2023, 4, 1), 
         'End Time__lte' : datetime(2023, 4, 2),
         'DefectReason__exists': True,
         '_limit': 10,
         '_only': columns[:30]}
TODO include other options in query 
df = cli.get_parts(**query)
```

### Downtimes
```python
query = {'Machine': machines[0],
         'End Time__gte' : datetime(2023, 4, 1), 
         'End Time__lte' : datetime(2023, 4, 2), 
         '_order_by': '-End Time'}
df = cli.get_downtimes(**query)
```

### KPIs
```python
cli.get_kpis()
```

```python
cli.get_kpis_for_asset(**asset_selection)
```

```python
cli.get_kpi_data_viz(machine_source, kpis, i_vars, time_selection, **optional_data_viz_query)
```

### Lines

```python
cli.get_line_data()
```


### Raw Data
```python
cli.get_raw_data()
```


### Cookbooks
```python
cli.get_cookbooks()
```

```python
cli.get_cookbook_top_results(recipe_group_id, limit)
```

```python
cli.get_cookbook_current_value(variables, minutes)
```

```python
cli.normalize_constraints(constraint_values)
```

