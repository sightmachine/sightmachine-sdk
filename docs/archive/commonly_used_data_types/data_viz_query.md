# Data Visualization Query
Data Viz Queries are used whenever the SDK calls our Data Visualization APIs.  The functions you call via SDK do some work on the query for you so this Query will look slightly different from the one our API uses directly.  We will break down each field in some more detail futher along in this doc but as an example a full Data Viz Query looks like the following:
```
{
  "asset_selection": {
    "machine_source": [
      "JB_AB_Lasercut_1"
    ],
    "machine_type": [
      "Lasercut"
    ]
  },
  "d_vars": [
    {
      "name": "quality",
      "aggregate": [
        "avg"
      ]
    }
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

## Asset_selection
Used to select the asset(s) you want to recieve data from see the [asset_selection doc](/docs/commonly_used_data_types/asset_selection.md) for more information.

## d_vars
The Dependent variables.  These will change depending on the entity you are trying to access.  But will always be a list in the following form:
```
    {
      "name": "quality",
      "aggregate": [
        "avg"
      ]
    }
```
### name
This is the name of dependent variable you wish to view.  This typically the name of a value we store on a machine or the name of a KPI.

### aggregate
This is how you wish to aggregate the data of the named value in the time_resolution you have selected. The options for this are:
* avg
* sum
* min
* max

## i_vars
The indepent variables.  These should typically be time based values that are stored on the machine_type you are using. They will always be a list in the following form:
```
{
      "name": "endtime",
      "time_resolution": "day",
      "query_tz": "America/Los_Angeles",
      "output_tz": "America/Los_Angeles",
      "bin_strategy": "user_defined2",
      "bin_count": 50
    }
```
### name
This is the name of idependent varaible you are using.

### time_resolution
This is optional and is how detailed of a time breakdown you want in the variable the options for time_resolution are as follows:
* year
* month
* week
* day
* hour
* minute
* second

### query_tz
This is optional and tells the system what time zone the query is in.

### output_tz
This is optional and tells the system what time zone to return the data in.

### bin_strategy
This is optional and tells the sytem how you wish to bin the data.  You have the following options:
* user_defined2
* none
* categorical

### bin_count
This is optoinal and tels the system how many bins you wish to put the data into.

## time_selection
This is the time frame you want to grab data from there are two different ways to make this time selection, Relative and Absolute

### Relative Time Selection
Relative Time Selections goes back from now a certain amount of time based on what you tell it.  The format for this time selection is the following:
```
{
    "time_type": "relative",
    "relative_start": 7,
    "relative_unit": "year",
    "ctime_tz": "America/Los_Angeles"
}
```
#### Time Type
For a relative time selection this needs to be set to "relative".

#### Relative Start
The amount of units from now you wish to go back to start your time selection.

#### Relative Unit
The unit of time you wish to go back from now.  Your options for this are as follows:
* year
* month
* week
* day
* hour
* minute
* second

#### ctime_tz
The time zone for your time selection

### Absolute Time Selection
Absolute Time Selections have a start and end time and will gather data from between the two.  The format for this time selection is as follows:
```
{
  "time_type": "absolute",
  "start_time": "2023-02-23T08:00:00.000Z",
  "end_time": "2023-03-01T21:35:35.499Z",
  "time_zone": "America/Los_Angeles"
}
```
#### Time Type
For absolute time selecitons this must be set to absolute.

#### Start Time
The time you wish to start the time selection at.

#### End Time
The time you wish to end the time selection at.

#### Time Zone
The time zone for the time selection.

## Where
This is optional.  It will narrow down the data return based on criteria given. The list will be anded together. This is a list in the following format:
```
{
    "name": "type__part_type",
    "op": "eq",
    "value": "EngineBlock"
}
```

### Name
The name of the field you are using in this criteria.

### Op
The type of operation you are doing.

### Value
The value to compare with the operation.

## db_mode
This is optional.  It will default to 'sql' and usually should be but we have a 'mongo' mode as well.  You will likely ever need to set this.