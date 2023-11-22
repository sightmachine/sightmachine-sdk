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
This function will get you the top runs of the recipe group you input. This function can be called using either of the two API calling styles:

#### Old Style API Call:

```
cli.get_cookbook_top_results(recipe_group_id, limit)
```

#### New Style API Call:

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

The two APIs exhibit fundamental similarities. While the old API exclusively supports positional arguments, the new API builds upon this foundation by allowing the use of both positional and keyword arguments. In the new API, all positional arguments from the old API can be employed as keyword arguments. If both positional and keyword arguments are provided, the keyword arguments take precedence.

For more info on the runs returned in each key see [runs](/docs/commonly_used_data_types/run.md).  The two parameter inputs do the following:

#### recipe_group_id
This is a string and is the only required parameter.  This is the id of the recipe group you are trying to return runs for.

#### limit
This is an int and is optional, if not entered it will default to 10.  This is the max number of runs you wish to return.

#### Example:

##### Old Style API Call:

```
runs = cli.get_cookbook_top_results("recipe_group_id", 1)
print(len(runs["runs"]))

# Output:
# 1
```

##### New Style API Call:

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
This function gets the current values of the fields passed into it. This function can be called using either of the two API calling styles:

#### Old Style API Call:

```
cli.get_cookbook_current_value(variables, minutes)
```

#### New Style API Call:

```
cli.get_cookbook_current_value(variables=variables, minutes=minutes)
```

The resulting output will something like:
```
[{'asset': 'JB_HM_Diecast_1', 'name': 'stats__InjectionPressureMin__val', 'values': {'latest': 35.1775016539}}]
```

The two APIs exhibit fundamental similarities. While the old API exclusively supports positional arguments, the new API builds upon this foundation by allowing the use of both positional and keyword arguments. In the new API, all positional arguments from the old API can be employed as keyword arguments. If both positional and keyword arguments are provided, the keyword arguments take precedence.

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

##### Old Style API Call:

```
value = cli.get_cookbook_current_value([{"asset": "test", "name": "test_field"}])
print(value)

# Output:
# [{'asset': 'test', 'name': 'test_field', 'values': {'latest': 42.42}}]
```

##### New Style API Call:

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