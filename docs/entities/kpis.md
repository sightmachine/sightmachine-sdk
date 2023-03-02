# KPIs

KPIs are user defined calculated fields in the Sight Machine software.

## Functions
The SDK has two functions related to KPIs.  The first of which allows a user to see which KPIs are availible for a particular asset.  The second makes use of our Data Visulation api which allows a user to see these KPIs over a timeframe.

### Get KPIs
This is the first KPI function allowing you to see which KPIs are availible for a particular asset.  In order to call this function you must first have a logged in client see the [quick start guide](/README.md) for more information on logging in.  Once you have a logged in client you can call the function as follows:

```
cli.get_kpis(**asset_selection)
```

For more info on [asset_selection](/docs/commonly_used_data_types/asset_selection.md) click on the previous link.  After a moment the SDK should return a list that looks something like this:

```
[{'name': 'quality', 'display_name': 'Quality', 'unit': '', 'type': 'continuous', 'data_type': 'float', 'stream_types': [], 'raw_data_field': ''},...]
```

In order to make use of the data viz function you'll need the name of the KPI you wish to get.

### Get KPI Data Viz
Once you have the name of the KPI you wish to access and a logged in client you can make a call to the data viz api with the following SDK function call:
```
cli.get_kpi_data_viz(**data_viz_query)
```

The d_vars section of your data_viz_query should include an d_var with the name of the KPI you wish to query.  For more information on [data_viz_queries](/docs/commonly_used_data_types/data_viz_query.md) click on the previous link.  After some time the SDK should return a list that looks something like this:
```
[{'i_vals': {'endtime': {'i_pos': 0, 'bin_no': 0, 'bin_min': '2022-10-20T00:00:00-07:00', 'bin_max': '2022-10-20T00:00:00-07:00', 'bin_avg': '2022-10-20T00:00:00-07:00'}}, 'd_vals': {'quality': {'avg': 95.18072289156626}}, '_count': 418, 'kpi_dependencies': {'quality': {'Output': 395.0, 'ScrapQuantity': 20.0}}},...]
```