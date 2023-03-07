# KPIs

KPIs are user defined calculated fields in the Sight Machine software.

## Functions
The SDK has three functions related to KPIs.  The first returns a list of all availible KPis.  The second of which allows a user to see which KPIs are availible for a particular asset.  The thrid makes use of our Data Visulation api which allows a user to see these KPIs over a timeframe.

### Get KPIs
This is the first KPI function allowing you to see which all KPIs.  In order to call this function you must first have a logged in client see the [quick start guide](/README.md) for more information on logging in.  Once you have a logged in client you can call the function as follows:

```
cli.get_kpis()
```
This will return a full list of KPIs which will look something like this example:
```
[{'name': 'performance', 'display_name': 'Performance', 'formula': '( IdealCycle / Recorded_time ) * 100 if ( Recorded_time > 0 ) else None', 'data_type': '', 'dependencies': [{'aggregate': 'sum', 'name': 'Recorded_time'}, {'aggregate': 'sum', 'name': 'IdealCycle'}]}, ...]
```

In order to make use of the data viz function you'll need the name of the KPI you wish to get.

### Get KPIs For Asset
This is the second KPI function allowing you to see which KPIs are availible for a particular asset.  Once you have a logged in client you can call the function as follows:

```
cli.get_kpis_for_asset(**asset_selection)
```

For more info on [asset_selection](/docs/commonly_used_data_types/asset_selection.md) click on the previous link.  After a moment the SDK should return a list that looks something like this:

```
[{'name': 'quality', 'display_name': 'Quality', 'unit': '', 'type': 'continuous', 'data_type': 'float', 'stream_types': [], 'raw_data_field': ''},...]
```

In order to make use of the data viz function you'll need the name of the KPI you wish to get.

### Get KPI Data Viz
Once you have the name of the KPI you wish to access and a logged in client you can make a call to the data viz api with the following SDK function call:
```
cli.get_kpi_data_viz(machine_source, kpis, i_vars, time_selection, **optional_data_viz_query)
```

After some time the SDK should return a list that looks something like this:
```
[{'i_vals': {'endtime': {'i_pos': 0, 'bin_no': 0, 'bin_min': '2022-10-20T00:00:00-07:00', 'bin_max': '2022-10-20T00:00:00-07:00', 'bin_avg': '2022-10-20T00:00:00-07:00'}}, 'd_vals': {'quality': {'avg': 95.18072289156626}}, '_count': 418, 'kpi_dependencies': {'quality': {'Output': 395.0, 'ScrapQuantity': 20.0}}},...]
```

There's two ways to call this function you can use a data_viz_query,For more information on [data_viz_queries](/docs/commonly_used_data_types/data_viz_query.md) click on the previous link, or have the function fill out the query for you by passing in a few variable we will now go over one at a time.

#### machine_source
This is a string and is the name of machine you wish to run a query on.

#### kpis
This is a list of the names of all the kpis you wish to run this query on.

#### i_vars
This is a list, this is the same as the i_vars object in the data_viz_query and is the axis you are querying the kpis against it will look like the following:
```
[
    {
      "name": "endtime",
      "time_resolution": "day",
      "query_tz": "America/Los_Angeles",
      "output_tz": "America/Los_Angeles"
    }
]
```

#### time_selection
This is an object, this is the same as the [time_selection](/docs/commonly_used_data_types/data_viz_query.md#time_selection) object in the data_viz_query and more info can be found at that link.  The most common form is the relative time selection and looks like this:
```
{
    "time_type": "relative",
    "relative_start": 7,
    "relative_unit": "day",
    "ctime_tz": "America/Los_Angeles"
}
```