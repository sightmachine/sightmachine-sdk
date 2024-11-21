# All Functions

TODO generate table of contents

TODO make sure I got all possible functions




## Create Client

To interact with Sight Machine data, you first need to initialize a client. This client handles the connection to the Sight Machine API.

The first step is to import the client submodule from the smsdk package. See the main [README.md](../README.md#installation) for installation instructions.

```python
from smsdk import client
```

Next, create an instance of the Client class. The 'tenant' argument should be set to the part of the tenant URL that preceeds '.sightmachine.io'. 

```python
tenant = 'demo-continuous'
cli = client.Client(tenant)
```

Finally, provide your API key and secret to initialize the connection. See [README.md -> Authenticating](../README.md#authenticating) for instructions for generating an API key and secret in-platform. The login function will return a boolean value indicating if the connection was successful. If it returns false, a few possible causes are invalid tenant name, incorrect API key and secret for that tenant, or lack of internet connection.

```python
success = cli.login('apikey', 
          key_id = api_key, 
          secret_id = api_secret)
if not success:
    raise AsseretionError("SDK login failed.")
```




## Client Functions

This section provides an overview of the various functions available in the Sight Machine SDK. These functions are designed to help you interact with and retrieve data from the Sight Machine platform efficiently. Each function is accompanied by example code snippets to demonstrate their usage and to help you integrate them into your own applications. Functions are split into general functions which pull general factory metadata, and data queries which pull tabular data from the various data models.


### General

Functions in this section are for pulling general factory metadata.


#### Machine Types

```python
cli.get_machine_type_names()
```

```python
cli.get_fields_of_machine_type(types[0])
```

#### Machines
```python
cli.get_machine_names(source_type)
```

machine to machine type
```python
cli.get_type_from_machine(machines[0])
```

#### Timezones
```python
cli.get_machine_timezone(machines[0])
```

#### Data Visualization Sharelinks



#### Lines



#### Choose Non-Production Workspace
WRONG FUNCTION cli.select_db_schema(schema_name=db_schema)


### Query Data
Functions in this section are for querying tabular data from our common data models: Cycles, Parts, Downtimes, KPI, Lines, and Raw Data. We also have support for pulling information from Cookbooks.

TODO reference Sight Machine docs for info on these models?
TODO mention that it only works if the model is setup? what happens if the model isn't set up?


#### Cycle Data
```python
cli.get_machine_schema()
```

```python
query = {'Machine': machines[0],
         'End Time__gte' : datetime(2023, 4, 1), 
         'End Time__lte' : datetime(2023, 4, 2), 
         '_order_by': '-End Time'}
TODO include other options in query 
df = cli.get_cycles(**query)
```

#### Parts
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

#### Downtimes
```python
query = {'Machine': machines[0],
         'End Time__gte' : datetime(2023, 4, 1), 
         'End Time__lte' : datetime(2023, 4, 2), 
         '_order_by': '-End Time'}
df = cli.get_downtimes(**query)
```

#### KPIs
```python
cli.get_kpis()
```

```python
cli.get_kpis_for_asset(**asset_selection)
```

```python
cli.get_kpi_data_viz(machine_source, kpis, i_vars, time_selection, **optional_data_viz_query)
```

#### Lines
TODO


#### Raw Data
TODO


#### Cookbooks
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

