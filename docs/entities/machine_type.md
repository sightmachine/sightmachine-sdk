# Machine Types
Machine Types are the schema for the various machines in a factory. 

## Functions

### get_fields_of_machine_type
The get_fields_of_machine_type function returns the fields of the machine schema for a specified machine type. This function can be called using either of the two methods of calling:

#### Using Positional Arguments
```
cli.get_fields_of_machine_type(machine_type, types, show_hidden)
```

#### Using Keyword Arguments
```
cli.get_fields_of_machine_type(machine_type=machine_type, types=types, show_hidden=show_hidden)
```

The only required field in this case is the machine_type, we will go over each variable in a second.  The function will return a pandas list that looks like the following:
```
[{'display_name': 'Machine', 'unit': '', 'type': 'categorical', 'data_type': 'string', 'stream_types': [], 'raw_data_field': '', 'name': 'machine__source'}, {'display_name': 'Cycle Start Time', 'unit': '', 'type': 'datetime', 'data_type': 'datetime', 'stream_types': [], 'raw_data_field': '', 'name': 'starttime'},..]
```

Both methods of calling the API are functionally equivalent. The first method exclusively uses positional arguments, while the second method employs named arguments. Providing both positional and keyword values for the same argument in an API call is not allowed. It will throw an error, causing the API call to fail.

#### machine_type
This is the name of the machine type that you are trying to grab the fields of.  This is the only required parameter for this function.

#### types
This is an optional parameter and is a list of strings.  If this is set the function will only return colomns that match the types given.  For example if we were to pass ['string'] as our types parameter in the previous example we would instead have returned:
```
[{'display_name': 'Machine', 'unit': '', 'type': 'categorical', 'data_type': 'string', 'stream_types': [], 'raw_data_field': '', 'name': 'machine__source'}]
```

#### show_hidden
This is an optional parameter and is a boolean.  There are a few fields we have set to be hiddden from our ui in our application and by defualt these are also hidden from the return in this function if set to True we will also return these fields.

#### Example:

##### Using Positional Arguments
```
machine_type = "Lasercut"
types = ["string", "float"]

fields = get_client.get_fields_of_machine_type(machine_type, types)
print(len(fields))

# Output:
# 29
```

##### Using Keyword Arguments
```
machine_type = "Lasercut"
types = ["string", "float"]

query = {
    "machine_type": machine_type,
    "types" : types,
    "show_hidden": True,
}

fields = get_client.get_fields_of_machine_type(**query)
print(len(fields))

# Output:
# 35
```
