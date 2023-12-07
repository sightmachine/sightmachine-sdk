# Cookbooks
Cookbooks are how the Sight Machine software provides recondemations and insights into various inputs and outcomes in a line.

## Functions
The Sight Machine SDK has several functions related to cookbooks allowing you to do things like look at the configuration of cookbooks and see the top runs of various recipes.

### Get Cookbooks
This functions gets the configuration of all cookbooks availible to your loged in user.  It is called like the following:
```
cli.get_cookbooks()
```
This will return a list of [cookbooks](/docs/commonly_used_data_types/cookbook.md), see link for more details on what that response looks like.

### Get Top Results
This function will get you the top runs of the recipe group you input. This function can be called using either of the two methods of calling:

#### Using Positional Arguments
```
cli.get_cookbook_top_results(recipe_group_id, limit)
```

#### Using Keyword Arguments
```
cli.get_cookbook_top_results(recipe_group_id=recipe_group_id, limit=limit)
```

The resulting output will something like:
```
[{
    "runs": [runs],
    "constraint_group": [runs]
}]
```

Both methods of calling the API are functionally equivalent. The first method exclusively uses positional arguments, while the second method employs named arguments. Providing both positional and keyword values for the same argument in an API call is not allowed. It will throw an error, causing the API call to fail.

For more info on the runs returned in each key see [runs](/docs/commonly_used_data_types/run.md).  The two parameter inputs do the following:

#### recipe_group_id
This is a string and is the only required parameter.  This is the id of the recipe group you are trying to return runs for.

#### limit
This is an int and is optional, if not entered it will default to 10.  This is the max number of runs you wish to return.

#### Example:

##### Using Positional Arguments
```
runs = cli.get_cookbook_top_results("recipe_group_id", 1)
print(len(runs["runs"]))

# Output:
# 1
```

##### Using Keyword Arguments
```
query = {
    "recipe_group_id" : "recipe_group_id",
    "limit" : 1
}

runs = cli.get_cookbook_top_results(**query)
print(len(runs["runs"]))

# Output:
# 1
```

### Get Current Value
This function gets the current values of the fields passed into it. This function can be called using either of the two methods of calling:

#### Using Positional Arguments
```
cli.get_cookbook_current_value(variables, minutes)
```

#### Using Keyword Arguments
```
cli.get_cookbook_current_value(variables=variables, minutes=minutes)
```

The resulting output will something like:
```
[{'asset': 'JB_HM_Diecast_1', 'name': 'stats__InjectionPressureMin__val', 'values': {'latest': 35.1775016539}}]
```

Both methods of calling the API are functionally equivalent. The first method exclusively uses positional arguments, while the second method employs named arguments. Providing both positional and keyword values for the same argument in an API call is not allowed. It will throw an error, causing the API call to fail.

The two parameter inputs do the following:

#### variables
A list of variables to get the value of, they are in the following form:
```
{'asset': 'JB_HM_Diecast_1', 'name': 'stats__InjectionPressureMin__val'}
```

##### asset
Asset is the name of the asset you are getting the field from.  It is usually a machine_name

##### name
Name is the name of the field you are grabing the value of.

#### minutes
This is an optional parameter and is passed in as integer.  This is the number of minutes you want to look back for the current value.

#### Example:

##### Using Positional Arguments
```
value = cli.get_cookbook_current_value([{"asset": "test", "name": "test_field"}])
print(value)

# Output:
# [{'asset': 'test', 'name': 'test_field', 'values': {'latest': 42.42}}]
```

##### Using Keyword Arguments
```
query = {
    "variables" : [{"asset": "test", "name": "test_field"}],
    "minutes" : 1440,
}

value = dt.get_cookbook_current_value(**query)

# Output:
# [{'asset': 'test', 'name': 'test_field', 'values': {'latest': 42.42}}]
```

### Normalize Constraints
This is a function to return a clean string version of constraints values. And is called like this:
```
cli.normalize_constraints(constraint_values)
```

#### constraints
The constraint values you wish to normalize, this only works for range values.