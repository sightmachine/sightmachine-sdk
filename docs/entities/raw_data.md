# Raw Data
Raw data records are an output from different machines in a facility. This doc is to explain how we can use this SDK to access the raw data records in readable format.


# Implementation in SDK

To implement this in SDK we had to add one more method get_raw_data() in smsdk/client.py.

Added support for selecting what fields the user wants to get from the raw data table including time_selection argument to filter out date range. 

This method is responsible for executing a POST method to v1/datatab/raw_data in MA project only after getting a user authenticated in smsdk.

### get_raw_data
To access raw data records from SDK user needs to log in smsdk using their api-key pair or username/password. After getting authenticated user will have a client object and using that client object they can call method like this- client.get_raw_data(“raw_data_sync_table“, “select_fields“, “time_selection“)

For example-

Taking an example of demo.sightmachine.io-

# Input
```
raw_data_table (str) = 'cycle_raw_data'

timeselection (dict) = {"time_type":"relative","relative_start":1,"relative_unit":"day","ctime_tz":"America/Los_Angeles"}

select (list) = ['stats__ConveyorInput__val','stats__ConveyorOutput__val']
```

#### Using Positional Arguments
```
cli.get_raw_data(raw_data_table, select, timeselection)
```

#### Using Keyword Arguments
```
cli.get_raw_data(raw_data_table=raw_data_table, fields=select, time_selection=timeselection)
```

And will return something like the following:
```
stats__Alarms__val  stats__BLOCKED__val  stats__ConveyorInput__val

None                  0.0                        0.0

None                  0.0                        0.0
```

Both methods of calling the API are functionally equivalent. The first method exclusively uses positional arguments, while the second method employs named arguments. Providing both positional and keyword values for the same argument in an API call is not allowed. It will throw an error, causing the API call to fail.


#### Example:

##### Using Positional Arguments
```
raw_data_table = RAW_DATA_TABLE
select = []
timeselection = {
    "time_type": "absolute",
    "start_time": "2023-10-18T18:30:00.000Z",
    "end_time": "2023-10-19T18:29:59.999Z",
    "time_zone": "America/Los_Angeles",
}

raw_data = get_client.get_raw_data(raw_data_table, select, timeselection)

print(raw_data.index.name)
print(raw_data.shape)

# Output:
# _id
# (400, 33)
```

##### Using Keyword Arguments
```
raw_data_table = RAW_DATA_TABLE
select = []
timeselection = {
    "time_type": "absolute",
    "start_time": "2023-10-18T18:30:00.000Z",
    "end_time": "2023-10-19T18:29:59.999Z",
    "time_zone": "America/Los_Angeles",
}

query = {
    "time_selection": timeselection,
    "raw_data_table": raw_data_table,
    "fields": select,
}

raw_data = get_client.get_raw_data(**query)

print(raw_data.index.name)
print(raw_data.shape)

# Output:
# _id
# (400, 33)
```

