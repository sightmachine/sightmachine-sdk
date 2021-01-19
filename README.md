# Sight Machine Python SDK

The Sight Machine software development kit (SDK) complements the Sight Machine platform by providing advanced users with the ability to retrieve data from the platform.  It is designed primarily for data analysts or data scientists who are interested in retrieving data from Sight Machine so they can perform their own custom analytics.  


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

### Retrieving Data

The typical workflow for getting data from Sight Machine is:

- Select the desired Machine Type
- Select the specific machine(s) of that type
- Retrieve data for the selected machine(s)

Note that you can skip to the final step if you already know the name of the machine(s), but the SDK provides various functions to also list
machine names and types.  These are particularly useful if creating an interactive application where the user selects their data sources from 
dropdown boxes.

#### Selecting Machine Types

The easiest way to get a list of all known Machine Types is with:

```
cli.get_machine_type_names()
```

This returns a python list with the machine type names.

#### Selecting Machines

The easiest way to get a list of Machines is with:

```
cli.get_machine_names(source_type=machine_type)
```

The *machine_type* variable would be a machine type name retrieved from a previous step.  The `source_type` argument is optional.  If you do not provide it, then
this function will return all machine names in the system.

#### Machine Schema

Although not requred, it is sometimes helpful to get a list of all stats available for a given machine.  That is done with the `get_machine_schema` function.  

```
cli.get_machine_schema(machine_name)
```

This returns a Pandas data frame with each stats Sight Machine internal name, display name, and type.  It takes an optional `types` argument, which filters the returned list to only a specific set of data types.  For example, to get the display names of all numeric stats on a machine, use:

```
cli.get_machine_schema(machine_name, types=['int', 'float'])['display'].tolist()
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

----


