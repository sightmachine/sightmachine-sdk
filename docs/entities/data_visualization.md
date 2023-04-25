# Data Visualization
Data Visualization or Data Viz is an application within the Sight Machine System that allows users to create various charts and graphs from data within the system.

## Functions

### Create Share Link
This function allows you to give it the "state" of a data viz and it will then return a link to the webapp allowing you to see this visualization in app.  It is called like this:
```
cli.create_share_link(assets, chartType, yAxis, xAxis, model, time_selection)
```

And will return something like this:
```
https://demo-discrete.sightmachine.io/#/analysis/datavis/s/t952360g
```

#### assets
This is a list of Machines_Names you are trying to get data from.  No matter the dataModel you choose you will always be able to simply give it a list however there are additional options when using the 'line' dataModel.  The simple list version looks like:
```
["F2_010_BodyMaker_1"]
```

When using the 'line' dataModel you have the options of passing in offsets in addition to the asset list.  In order to do this assets has to be an object with both an 'assetOffsets' and 'assets' field which looks like the following
```
{
    'assetsOffsets': {
        'F2_010_BodyMaker_1': {
            'interval': 1,
            'period': "minutes"
        }
    },
    'assets': ["F2_010_BodyMaker_1"]
}
```

#### chartType
This is a string telling the system what type of visualization you wish to see currently we support:
```
'line'
'bar'
```

#### yAxis
This is the yAxis of the chart it is either an object or a list of objects of the fields(or kpis) you wish to display on the yAxis.  Each field(or kpi) only needs it's id.  Note kpis only work with the 'kpi' data model.  It will look like for non-line models:
```
{"id": "stats__0_BM: CPM__val"}
```

When using the line model we also need the machine this field comes from and looks like:
```
{'field': "stats__0_BM 008: Cans Out__val", 'machineName': "F2_010_BodyMaker_1"}
```

#### xAxis
This the is the xAxis of the chart and will defualt to 'endtime'.  Just like the yAxis all that is needed is the id of the field you wish to use:
```
{"id": "endtime"}
```

#### model
This is a string and is the data model you wish to use.  It will default to 'cycle'.  Currently we support:
```
'cycle'
'kpi'
'line'
```

#### time_selection
This works like other time selections, more details [here](/docs/commonly_used_data_types/data_viz_query.md#time_selection).  This defaults to one week relative if not set.

