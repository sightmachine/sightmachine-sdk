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
This function will get you the top runs of the recipe group you input. This function can be called using either of the two APIs:

#### Old API:

```
cli.get_cookbook_top_results(recipe_group_id, limit)
```

#### New API:

```
cli.get_cookbook_top_results(recipe_group_id=recipe_group_id, limit=limit)
```

This will return the following:
```
[{
    "runs": [runs],
    "constraint_group": [runs]
}]
```

In the new API, all the positional arguments from the old API can be used as keyword arguments. If both positional arguments and keyword arguments are given, positional arguments will be neglected.

For more info on the runs returned in each key see [runs](/docs/commonly_used_data_types/run.md).  The two parameter inputs do the following:

#### recipe_group_id
This is a string and is the only required parameter.  This is the id of the recipe group you are trying to return runs for.

#### limit
This is an int and is optional, if not entered it will default to 10.  This is the max number of runs you wish to return.

### Get Current Value
This function gets the current values of the fields passed into it. This function can be called using either of the two APIs:

#### Old API:

```
cli.get_cookbook_current_value(variables, minutes)
```

#### New API:

```
cli.get_cookbook_current_value(variables=variables, minutes=minutes)
```

It returns something like:
```
[{'asset': 'JB_HM_Diecast_1', 'name': 'stats__InjectionPressureMin__val', 'values': {'latest': 35.1775016539}}]
```

In the new API, all the positional arguments from the old API can be used as keyword arguments. If both positional arguments and keyword arguments are given, positional arguments will be neglected.

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
This is an optional parameter and is passed in as integer.  This is the number of minutes you want to look bak for the current value.

### Normalize Constraints
This is a function to return a clean string version of constraints values. And is called like this:
```
cli.normalize_constraints(constraint_values)
```

#### constraints
The constraint values you wish to normalize, this only works for range values.