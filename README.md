# Sight Machine Python SDK

The Sight Machine software development kit (SDK) complements the Sight Machine platform by providing advanced users with the ability to retrieve data from the platform.  It is designed primarily for data analysts or data scientists who are interested in retrieving data from Sight Machine so they can perform their own custom analytics.  

For detailed documentation about each function, please refer to [docs/README.md](#docs/README.md).

## Installation

It is easiest to install using pip directly from GitHub.  From a shell/command prompt enter:

```
pip install git+https://github.com/sightmachine/sightmachine-sdk.git
```

To confirm that it successfully installed, in a python script or notebook enter:

```
import smsdk
```

 
## Quick Start

The following quick start guide will get you up and running with a common use case of connecting to the Sight Machine platform, authenticating,
selecting the desired machines, and retrieving data for cycles on those machines.

### Client

When accessing Sight Machine via the SDK, the first step is always to initialize a Client.  This is essentially your connection to the database.  A client
will point to the name of the tenant on Sight Machine.  For example, if you access Sight Machine at the URL *mycompany*.sightmachine.io, then *mycompany* is 
the name of the tenant you will use. For purposes of this Quick Start documentation, we will use demo as the tenant name.

To initialize a Client: 

```
from smsdk import client
tenant = 'demo'
cli = client.Client(tenant)
```

### Authenticating

Sight Machine currently supports two methods of authentication via the SDK:
- *basic*: Username and password authentication.  This is the preferred method if you are accessing the data in an interactive format such as Jupyter notebooks
or user interactive scripts.
- *apikey*: Using an API Key generated in the platform.  This method is used for automated data retrievals where there is no user to interact with a password prompt.  To generate an API Key:
  - Log into the Sight Machine Platform
  - From the hamburger menu (three lines icon) on the right, click the Profile link
  - In the API Key section, click the button that says "+ Create API Key"
  - It will generate the API Secret and Key.  You will need both keys to authenticate.  

  
For basic authentication:
```
username = my_email_address
password = my_really_secure_password

cli.login('basic', email=username, password=password)
```

For API Key authentication:
```
key = api_key_from_platform
secret = api_secret_from_platform

cli.login('apikey', secret_id=secret, key_id=key)
```

### Proxy Servers and CA Certs

If your network uses a proxy server to access the Internet, please set environment variables for 
 HTTP_PROXY and HTTPS_PROXY to point to your proxy server.  

```
HTTP_PROXY="http://10.0.1.2:8080"
HTTPS_PROXY="http://10.0.1.2:8080"
```

Similarly, if you need to use your own CA Certificates, set the CURL_CA_BUNDLE environment variable specifying the path to those certificates.

```
CURL_CA_BUNDLE="/path/to/my/certificates"
```

### Selecting database schema
By default, the production pipeline schema will be considered to retrive data from the tenant.
To select a particular development pipeline schema you can use following function call:

```
db_schema = pipeline_id 
cli.select_db_schema(schema_name=db_schema)
```

### Retrieving Data

The typical workflow for getting data from Sight Machine is:

- Select the desired Machine Type
- Select the specific machine(s) of that type
- Retrieve data for the selected machine(s)

Note that you can skip to the final step if you already know the name of the machine(s), but the SDK provides various functions to also list
machine names and types.  These are particularly useful if creating an interactive application where the user selects their data sources from 
dropdown boxes.

#### Selecting Machine Types

To obtain a list of all known Machine Type names, This can be invoked using either of the two methods of calling:

##### Using Positional Arguments

```
cli.get_machine_type_names(clean_strings_out)
```

##### Using Keyword Arguments

```
cli.get_machine_type_names(clean_strings_out=clean_strings_out)
```

The function returns a Python list containing the names of machine types.

An optional flag, `clean_strings_out`, determines the format of the returned list. If set to true, the list will use UI-based display names. If set to false, the list will contain Sight Machine internal machine types. If this flag is not provided, the function will default to returning UI-based display names.

Both methods of calling the API are functionally equivalent. The first method exclusively uses positional arguments, while the second method employs named arguments. Providing both positional and keyword values for the same argument in an API call is not allowed. It will throw an error, causing the API call to fail.

##### Example:

###### Using Positional Arguments

```
types_ui_based = cli.get_machine_type_names()
print(types_ui_based)

# Output:
# ['Lasercut', 'Pick & Place', 'Diecast', 'Fusion']
```

###### Using Keyword Arguments

```
query = {
    "clean_strings_out" : False
}

types_internal = cli.get_machine_type_names(**query)
print(types_internal)

# Output:
# ['Lasercut', 'PickAndPlace', 'Diecast', 'Fusion']
```

#### Selecting Machines

The most straightforward way to obtain a list of Machines is by utilizing  either of the two methods of calling:

##### Using Positional Arguments

```
cli.get_machine_names(machine_type, clean_strings_out)
```

##### Using Keyword Arguments

```
cli.get_machine_names(source_type=machine_type, clean_strings_out=clean_strings_out)
```

The *machine_type* variable would be a machine type name retrieved from a previous step.  The `source_type` argument is optional.  If you do not provide it, then this function will return all machine names in the system.

An optional flag, `clean_strings_out`, determines the format of the returned list. If set to true, the list will use UI-based display names. If set to false, the list will contain Sight Machine internal machine types. If this flag is not provided, the function will default to returning UI-based display names.

Both methods of calling the API are functionally equivalent. The first method exclusively uses positional arguments, while the second method employs named arguments. Providing both positional and keyword values for the same argument in an API call is not allowed. It will throw an error, causing the API call to fail.

##### Example:

###### Using Positional Arguments

```
machine_names_ui_based = cli.get_machine_names("Lasercut", True)
print(machine_names_ui_based[0:3])

# Output:
# ['Lima - Lasercut 1', 'Carmel - Lasercut 2', 'Carmel - Lasercut 5']
```

###### Using Keyword Arguments

```
query = {
    "source_type" : "Lasercut",
    "clean_strings_out" : False,
}

machine_names_internal = cli.get_machine_names(**query**)
print(machine_names_internal[0:3])

# Output:
# ['JB_LM_Lasercut_1', 'JB_CA_Lasercut_2', 'JB_CA_Lasercut_5']
```

#### Machine Types

The most straightforward way to obtain a list of Machine Types and associated Metadata is by utilizing either of the two methods of calling:

##### Using Positional Arguments

```
cli.get_machine_types(machine_type)
```

##### Using Keyword Arguments

```
cli.get_machine_types(source_type=machine_type)
```

The *machine_type* variable would be a machine type name retrieved from a previous step.  The `source_type` argument is optional.  If you do not provide it, then this function will return all machine types and associated metadata in the system.

Both methods of calling the API are functionally equivalent. The first method exclusively uses positional arguments, while the second method employs named arguments. Providing both positional and keyword values for the same argument in an API call is not allowed. It will throw an error, causing the API call to fail.

##### Example:

###### Using Positional Arguments

```
machine_types = get_client.get_machine_types()
print(machine_types.shape)

# Output:
# (114, 25)
```

###### Using Keyword Arguments

```
query = {
    "source_type" : "Lasercut",
}

machine_types = cli.get_machine_types(**query)
print(machine_types.shape)

# Output:
# (29, 25)
```

#### Machine Schema

It is sometimes helpful to get a list of all stats available for a given Machine.  This function can be invoked using either of the two methods of calling:

##### Using Positional Arguments

```
cli.get_machine_schema(machine_name, types,show_hidden, return_mtype)
```

##### Using Keyword Arguments

```
cli.get_machine_schema(machine_source=machine_name, types=types, show_hidden=show_hidden, return_mtype=return_mtype)
```

This returns a Pandas DataFrame with each stat's Sight Machine internal name, display name, and type. Except for `machine_source`, all the other three arguments are optional. The argument `types` specifies the list of data types used to filter the returned data set. By default, the list is empty.

The other optional argument `show_hidden` is used to control the display of hidden content in the data set. The default value is set to False.

The final optional argument `return_mtype` has a default value of False. If set to True, the API will return a tuple of (machine type, Pandas DataFrame) instead of just the Pandas DataFrame.

Both methods of calling the API are functionally equivalent. The first method exclusively uses positional arguments, while the second method employs named arguments. Providing both positional and keyword values for the same argument in an API call is not allowed. It will throw an error, causing the API call to fail.

##### Example:

###### Using Positional Arguments

```
fields = get_client.get_machine_schema(machine)
print(fields.shape)

fields = get_client.get_machine_schema(machine, ["string", "int"], False, True)
print(fields[0])
print(fields[1].shape)

# Output:
# (35, 13)
# Lasercut
# (16, 13)
```

###### Using Keyword Arguments

```
query = {
    "machine_source" : machine,
    "types" : ["string", "int"],
    "show_hidden" : False,
    "return_mtype" : True
}

fields = get_client.get_machine_schema(**query)
print(fields[0])
print(fields[1].shape)

# Output:
# Lasercut
# (16, 13)
```

#### Retrieving Cycle Data

Pulling cycle data from the platform requires a slightly more complex query structure.  Queries are formulated as a dictionary of criteria.  The structure
is similar to that used in MongoEngine where operators are appended to the field name.  For example, if you want to query for temperature greater than 100, the
equivalent key/value pair is `{'temperature__gt': 100}`.

- Note: one current limitation is that the Sight Machine API does not support logical OR when combining query parameters.  

```
query = {'Machine': 'My Machine',
         'End Time__gte' : datetime(2017, 8, 6), 
         'End Time__lte' : datetime(2017, 8, 7), 
         '_order_by': '-End Time'}
cli.get_cycles(**query)
```

IMPORTANT: We highly recommend setting time filters and ordering in all queries of the cycle model to ensure consistent data values are returned.  This minimizes the chances that changes to the database while the queries are running will result in data inconsistencies.

You can use the `_only` parameter to provide a list of column names to retrieve.  If you do not
specify the list of columns, it will default to pulling the first 50 columns of data from the machine type.  This is to prevent unexpectedly large and slow queries for machines with many columns of data.  To pull more than these 50 columns, please specificy all desired columns.

----
