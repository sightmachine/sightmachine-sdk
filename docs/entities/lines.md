# Lines
Lines are a set of connected machines.  The Sight Machine system has a data model that acounts for this connection.  

## Functions
The SDK has two functions that allow you access the lines in a factory and query data from them.

### Get Lines
This function shows you the lines that are availible to you.  It is called in the following way:
```
cli.get_lines()
```

This will return a list of lines and will like the following:
```
[{'id': 'F2_CANNING_L1', 'factory_id': 'ETL3_Ann Arbor Facility', 'display_name': 'F2 Canning Line 1', 'display_order': [], 'name': 'F2_CANNING_L1', 'order': 1, 'machine': [{'name': 'F2_010_BodyMaker_1', 'id': '92d8ed9b95746fd4ca631fe8'}, {'name': 'F2_010_BodyMaker_2', 'id': '466af0cd444ee73cad2a88c3'}, {'name': 'F2_010_BodyMaker_3', 'id': '91c4e2f9c24df37efaa9d182'}, {'name': 'F2_010_BodyMaker_4', 'id': '974ae3282252b07f068e9bfb'}, {'name': 'F2_010_BodyMaker_5', 'id': 'd48b29e39039636d368c31ff'}, {'name': 'F2_010_BodyMaker_6', 'id': 'f44ca977b67ed15e2802ea61'}, {'name': 'F2_010_BodyMaker_7', 'id': 'a9bc9ff53775885018b05f0c'}, {'name': 'F2_010_BodyMaker_8', 'id': 'a3286fb9d828857f2f4fdda8'}, {'name': 'F2_010_Washer_1', 'id': '415923d3a1d6eb7f5c3cf723'}, {'name': 'F2_010_CupPress_1', 'id': '8594f442b999f9ac627fc3ac'}, {'name': 'F2_010_Decorator_1', 'id': 'c3c0177e90204434a9120a0d'}, {'name': 'F2_010_Lacquer_1', 'id': 'aea383c35f0bc970822d39e6'}, {'name': 'F2_010_IBO_1', 'id': 'c54c4ccf6028b0a7a61052f1'}, {'name': 'F2_010_Necker_1', 'id': 'd9297c71823e69f0826e2499'}, {'name': 'F2_010_Lacquer_2', 'id': 'e627157c72528058a52d8e18'}, {'name': 'F2_010_Lacquer_3', 'id': '993ee9fb99a927751bb31daf'}, {'name': 'F2_010_Lacquer_4', 'id': 'e6d39f26400ff63e36b80fb7'}, {'name': 'F2_010_Lacquer_5', 'id': '9d4fe2e56cc7cc851746b600'}, {'name': 'F2_010_Lacquer_6', 'id': 'b48ed73ca132a501557dc1cf'}, {'name': 'F2_010_Lacquer_7', 'id': '98a62ec7d452a30b82ac7eda'}, {'name': 'F2_010_Pressco_1', 'id': '1de83e461094d63c5d252306'}]},...]
```

### Get Line Data
This function allows you to pull data from our line model.  This function can be called using either of the two methods of calling:

#### Using Positional Arguments
```
cli.get_line_data(assets, fields,  time_selection, asset_time_offset, filters, limit, offset)
```

#### Using Keyword Arguments
```
cli.get_line_data(assets=assets, fields=fields,  time_selection=time_selection, asset_time_offset=asset_time_offset, filters=filters, limit=limit, offset=offset)
```

It will return something like:
```
[{'F2_010_BodyMaker_1:starttime': '2023-04-05 16:57:00.000000', 'F2_010_BodyMaker_2:starttime': '2023-04-05 16:57:00.000000', 'F2_010_BodyMaker_3:starttime': '2023-04-05 16:57:00.000000', 'F1_010_Coolant_1:starttime': None, 'SHARED:offset_endtime': '2023-04-05 16:58:00.000000', 'F2_010_BodyMaker_1:stats__0_BM 008: Cans Out__val': 20920.0, '_id': 'dwLUrptRdQBdjzoBbtgEqh1KvcsIHHc1GefojYTNWXA='}...]
```

Both methods of calling the API are functionally equivalent. The first method exclusively uses positional arguments, while the second method employs named arguments. Providing both positional and keyword values for the same argument in an API call is not allowed. It will throw an error, causing the API call to fail.

#### assets
A required field, this is a list of strings where the strings used are all machine_names.  You can use machines from different lines.
```
["F2_010_BodyMaker_1", "F2_010_BodyMaker_2", "F2_010_BodyMaker_3", "F1_010_Coolant_1"]
```

#### fields
A required field, this is a list of objects telling the API which fields to grab on each machine the object takes the form of
```
{"asset": "F2_010_BodyMaker_1", "name": "stats__0_BM 008: Cans Out__val"}
```
Where 'asset' is a machine_name used in assets and 'name' is the name of a field on that machine.

#### time_selection
This is the same time selection we use in other places more details can be found [here](/docs/commonly_used_data_types/data_viz_query.md#time_selection).  It defaults to one day if none is given and can look like this:
```
{
    "time_type": "relative",
    "relative_start": 7,
    "relative_unit": "day",
    "ctime_tz": "America/Los_Angeles"
}
```

#### asset_offset
This is used to set offsets between machines in a line.  This is optional and will defualt to no offset if not given.  This is a dictionary that looks like this:
```
{"F2_010_BodyMaker_2": {'interval': 1, 'period': 'minutes'}}
```

#### filters
This is optional and a way to to filter the data.  This a list of objects that each look like the following:
```
{
    "asset": "F2_010_BodyMaker_1",
    "name": "stats__0_BM 008: Cans Out__val",
    "op": "gt",
    "value": 35200.0
}
```

##### asset
The name of the asset this filter is looking at. This will be a machine_name.

##### name
The name of the field you are looking at for this machine.

##### op
The operation you are filtering with.  Options inclue:
lt: less than
gt: greater than
lte: less than or equal to
gte: greater than or equal to
eq: equal to
in: in
ne: not equal to

##### value
The value you are comparing the field to.

#### limit
The max number of records you wish to get.

#### offset
The number of records at the begining you wish to skip.

#### Example:

##### Using Positional Arguments
```
assets = [MACHINE]
fields = [
    {"asset": MACHINE, "name": FIELD_NAME1},
    {"asset": MACHINE, "name": FIELD_NAME2},
]

time_selection = {
    "time_type": "absolute",
    "start_time": START_DATETIME,
    "end_time": END_DATETIME,
    "time_zone": TIME_ZONE,
}

filters = [
    {
        "asset": MACHINE,
        "name": FIELD_NAME2,
        "op": "gte",
        "value": MIN_PRESSURE,
    }
]

df = get_client.get_line_data(
    assets, fields, time_selection, filters=filters, limit=MAX_ROWS
)
print(len(df))

# Output:
# 14
```

##### Using Keyword Arguments
```
assets = [MACHINE]
fields = [
    {"asset": MACHINE, "name": FIELD_NAME1},
    {"asset": MACHINE, "name": FIELD_NAME2},
]

time_selection = {
    "time_type": "absolute",
    "start_time": START_DATETIME,
    "end_time": END_DATETIME,
    "time_zone": TIME_ZONE,
}

filters = [
    {
        "asset": MACHINE,
        "name": FIELD_NAME2,
        "op": "gte",
        "value": MIN_PRESSURE,
    }
]

query = {
    "assets": assets,
    "fields": fields,
    "time_selection": time_selection,
    "filters": filters,
    "limit": MAX_ROWS,
}

df = get_client.get_line_data(**query)
print(len(df))

# Output:
# 14
```

### Get Line Data Lineviz
This function allows you to pull data from our line model via lineviz API.  This function can be called using either of the two methods of calling:

#### Using Positional Arguments
```
cli.get_line_data_lineviz(assets, d_vars, i_vars, time_selection, asset_time_offset, filters)
```

#### Using Keyword Arguments
```
cli.get_line_data_lineviz(assets=assets, d_vars=d_vars, i_vars=i_vars, time_selection=time_selection, asset_time_offset=asset_time_offset, filters=filters)
```

It will return something like:
```
[
  {
    "i_vals": [
      {
        "name": "offset_endtime",
        "asset": "SHARED",
        "i_pos": 0,
        "value": {
          "bin_no": 0,
          "bin_min": "2024-07-06T00:00:00+00:00",
          "bin_max": "2024-07-06T00:00:00+00:00",
          "bin_avg": "2024-07-06T00:00:00+00:00"
        }
      }
    ],
    "d_vals": [
      {
        "name": "quality",
        "asset": "F3_Paper_Mill_PM1_Production_Status",
        "d_pos": 0,
        "value": {
          "avg": 90.5265124361114
        },
        "kpi": {
          "dependencies": {
            "reject_tons": 0.9635,
            "good_tons": 1380818.9,
            "random": 1445.0002659794823
          },
          "formula": "good_tons / (good_tons + (reject_tons + (random * 100))) * 100 if (good_tons + (reject_tons + (random * 100))) > 0 else None",
          "aggregates": {
            "reject_tons": "sum",
            "good_tons": "sum",
            "random": "sum"
          }
        },
        "type": "kpi"
      },
      {
        "name": "stats__32RL1BWTACT__val",
        "asset": "F1_Paper_Mill_PM2_Production_Status",
        "d_pos": 1,
        "value": {
          "avg": 70.23743333551619
        },
        "type": "continuous"
      }
    ],
    "_count": 2880
  },
  {
    "i_vals": [
      {
        "name": "offset_endtime",
        "asset": "SHARED",
        "i_pos": 0,
        "value": {
          "bin_no": 1,
          "bin_min": "2024-07-07T00:00:00+00:00",
          "bin_max": "2024-07-07T00:00:00+00:00",
          "bin_avg": "2024-07-07T00:00:00+00:00"
        }
      }
    ],
    "d_vals": [
      {
        "name": "quality",
        "asset": "F3_Paper_Mill_PM1_Production_Status",
        "d_pos": 0,
        "value": {
          "avg": 92.36746206062107
        },
        "kpi": {
          "dependencies": {
            "reject_tons": 313.66733,
            "good_tons": 1177192.4,
            "random": 969.6047504117041
          },
          "formula": "good_tons / (good_tons + (reject_tons + (random * 100))) * 100 if (good_tons + (reject_tons + (random * 100))) > 0 else None",
          "aggregates": {
            "reject_tons": "sum",
            "good_tons": "sum",
            "random": "sum"
          }
        },
        "type": "kpi"
      },
      {
        "name": "stats__32RL1BWTACT__val",
        "asset": "F1_Paper_Mill_PM2_Production_Status",
        "d_pos": 1,
        "value": {
          "avg": 72.70377143305424
        },
        "type": "continuous"
      }
    ],
    "_count": 1954
  }
]
```

Both methods of calling the API are functionally equivalent. The first method exclusively uses positional arguments, while the second method employs named arguments. Providing both positional and keyword values for the same argument in an API call is not allowed. It will throw an error, causing the API call to fail.

#### assets
A required field, this is a list of strings where the strings used are all machine_names.  You can use machines from different lines.
```
["F3_Paper_Mill_PM1_Production_Status", "F1_Paper_Mill_PM2_Production_Status"]
```

#### d_vars
The Dependent variables.  These will change depending on the entity you are trying to access.  But will always be a list in the following form:
```
[
    {
      "name": "quality",
      "asset": "F3_Paper_Mill_PM1_Production_Status",
      "aggregate": [
        "avg"
      ],
      "type": "kpi"
    },
    {
      "name": "stats__32RL1BWTACT__val",
      "asset": "F1_Paper_Mill_PM2_Production_Status",
      "aggregate": [
        "avg"
      ],
      "type": "continuous"
    }
]
```


#### i_vars
The indepent variables.  These should typically be time based values that are stored on the machine_type you are using. They will always be a list in the following form:
```
[
    {
      "name": "offset_endtime",
      "asset": "SHARED",
      "time_resolution": "day",
      "query_tz": "UTC",
      "output_tz": "UTC",
      "bin_strategy": "user_defined2",
      "bin_count": 50
    }
]
```


#### time_selection
This is the same time selection we use in other places more details can be found [here](/docs/commonly_used_data_types/data_viz_query.md#time_selection).  It defaults to one day if none is given and can look like this:
```
{
    "time_type": "relative",
    "relative_start": 7,
    "relative_unit": "day",
    "ctime_tz": "America/Los_Angeles"
}
```


#### asset_time_offset
This is used to set offsets between machines in a line.  This is optional and will defualt to no offset if not given.  This is a dictionary that looks like this:
```
{
    "F3_Paper_Mill_PM1_Production_Status": {
      "interval": 0,
      "period": "minutes"
    },
    "F1_Paper_Mill_PM2_Production_Status": {
      "interval": 0,
      "period": "minutes"
    }
}
```


#### filters
This is optional and a way to to filter the data.  This a list of objects that each look like the following:
```
{
    "asset": "F2_010_BodyMaker_1",
    "name": "stats__0_BM 008: Cans Out__val",
    "op": "gt",
    "value": 35200.0
}
```

##### asset
The name of the asset this filter is looking at. This will be a machine_name.

##### name
The name of the field you are looking at for this machine.

##### op
The operation you are filtering with.  Options inclue:
lt: less than
gt: greater than
lte: less than or equal to
gte: greater than or equal to
eq: equal to
in: in
ne: not equal to

##### value
The value you are comparing the field to.
