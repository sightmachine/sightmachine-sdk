# All Functions

This document provides an overview of the various functions available in the Sight Machine SDK. These functions are designed to help you interact with and retrieve data from the Sight Machine platform efficiently. Each function is accompanied by example code snippets to demonstrate their usage and to help you integrate them into your own applications. 

Functions are split into general functions which pull general factory metadata, and data queries which pull tabular data from the various data models. All functions are methods of the client object, which needs to be instantiated first.


TODO generate table of contents

TODO make sure I got all important functions

TODO make sure I have all the sections for each function




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

**Examples:**

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

**Examples:**


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

Get a list of all machines and their metadata. If you only want to get a list of available machines, see get_machine_names().

```python
cli.get_machines()
```

Returns:
> - **Pandas DataFrame**
>   - A table with metadata about each machine. Notable info items are machine UI-based display name, Sight Machine internal name, machine type, and factory location. There are 10 total columns.

**Examples:**

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

**Examples:**

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



```python
cli.get_machine_schema()
```





#### Client.get_type_from_machine

machine to machine type
```python
cli.get_type_from_machine(machine)
```



#### Client.get_machine_source_from_clean_name
```python
cli.get_machine_source_from_clean_name(machine)
```









### Lines
---



### Other
---

#### Client.get_machine_timezone
```python
cli.get_machine_timezone(machine)
```


TODO Data Visualization Sharelinks




### Use Non-Production Workspace
---
WRONG FUNCTION cli.select_db_schema(schema_name=db_schema)




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
TODO


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

