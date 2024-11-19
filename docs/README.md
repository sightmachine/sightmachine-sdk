# All Functions

- [Create Client](#create-client)
- [Client Functions](#client-functions)
    - [General](#general)
        - [Choose Non-Production Workspace](#choose-non-production-workspace)
        - [Machine Types](#machine-types)
        - [Machines](#machines)
        - [Timezones](#timezones)
        - [Data Visualization](#data-visualization)
        - [Lines](#lines)
    - [Query Data](#query-data)
        - [Cycle Data](#cycle-data)
        - [Parts](#parts)
        - [Downtimes](#downtimes)
        - [KPIs](#kpis)
        - [Raw Data](#raw-data)
        - [Cookbooks](#cookbooks)


## Create Client

from smsdk import client
cli = client.Client(tenant)
cli.login('apikey', 
          key_id = api_key, 
          secret_id = api_secret)


## Client Functions



### General


#### Choose Non-Production Workspace
WRONG FUNCTION cli.select_db_schema(schema_name=db_schema)

#### Machine Types
cli.get_machine_type_names()


cli.get_fields_of_machine_type(types[0])

#### Machines
cli.get_machine_names(source_type)

machine to machine type
cli.get_type_from_machine(machines[0])

#### Timezones
cli.get_machine_timezone(machines[0])

#### Data Visualization



#### Lines



### Query Data


#### Cycle Data
cli.get_machine_schema()

query = {'Machine': machines[0],
         'End Time__gte' : datetime(2023, 4, 1), 
         'End Time__lte' : datetime(2023, 4, 2), 
         '_order_by': '-End Time'}
TODO include other options in query 
df = cli.get_cycles(**query)

#### Parts
cli.get_part_type_names()
cli.get_part_schema(part_type)

query = {'Part': part_type,
         'End Time__gte' : datetime(2023, 4, 1), 
         'End Time__lte' : datetime(2023, 4, 2),
         'DefectReason__exists': True,
         '_limit': 10,
         '_only': columns[:30]}
TODO include other options in query 
df = cli.get_parts(**query)

#### Downtimes
query = {'Machine': machines[0],
         'End Time__gte' : datetime(2023, 4, 1), 
         'End Time__lte' : datetime(2023, 4, 2), 
         '_order_by': '-End Time'}
df = cli.get_downtimes(**query)

#### KPIs
cli.get_kpis()
cli.get_kpis_for_asset(**asset_selection)
cli.get_kpi_data_viz(machine_source, kpis, i_vars, time_selection, **optional_data_viz_query)

#### Raw Data

#### Cookbooks
cli.get_cookbooks()
cli.get_cookbook_top_results(recipe_group_id, limit)
cli.get_cookbook_current_value(variables, minutes)
cli.normalize_constraints(constraint_values)

