# Cookbook
 This is how a cookbook is stored in the data base it looks like this:
 ```
{
    "hash": "hash",
    "name": "name",
    "assetNames": ['machine names'],
    "key_constraint":{
        'field': {
            'fieldName': 'stats__Cylinders__val',
            'machineId': 'e2df2b4f115b763f45d04fa2',
            'machineName': 'JB_HM_Diecast_1',
            'machineDisplayName': 'Hamilton - Diecast 1',
            'fieldType': 'categorical',
            'machineType': 'Diecast',
            'fieldDisplayName': 'Cylinders',
            'fieldUnit': ''
        }, 
        'valueMap': {'4': 1, '6': 0}
    }
    "recipe_groups": [
        recipe_groups
    ]
    "metadata":{'created_by': {'id': '5a1c9f9798214579dacc917a', 'email': 'ahome@sightmachine.com', 'metadata': {'first_name': 'Andrew', 'last_name': 'Home', 'tenant': 'demo'}}},
    "updatetime": '2023-03-16 17:48:55.355000',
    "assets": [],
    "id": '63ab6b263fa4880c06334b03'

}
 ```

 ## Hash
 A hash of the cookbook object.

 ## name
 The name of the cookbook.

 ## assetNames
 A list of names of assets used in this cookbook these are often just machine_names.

 ## key_constraint
 The field that specfices the product.  This also how the system knows which recipe_group to use.

 ### field
 This is detailed information on the field being used as the Key Constraint for more info see [levers](#levers).

 ### valueMap
 This how the system maps the values of the key constraint on to recipe groups.  Value for each key is the index of the recipe group to use.

 ## recipe_groups
 A list of recipe groups,  They look like the following and will be described in more details
 ```
 {
    "id": "id"
    "values": [1],
    "runBoundaries": [],
    "maxDuration": {'isEnabled': False, 'minimum': 0, 'unit': 'second'},
    "topRun": 10,
    "constraints": [],
    "levers": [{'fieldName': 'stats__AluminumTempAvg__val', 'machineId': 'e2df2b4f115b763f45d04fa2', 'machineName': 'JB_HM_Diecast_1', 'machineDisplayName': 'Hamilton - Diecast 1', 'fieldType': 'continuous', 'machineType': 'Diecast', 'fieldDisplayName': 'AluminumTemp - Average', 'fieldUnit': 'celsius'},...],
    "outcomes": [{'field': {'fieldName': 'quality', 'machineId': 'e2df2b4f115b763f45d04fa2', 'machineName': 'JB_HM_Diecast_1', 'machineDisplayName': 'Hamilton - Diecast 1', 'fieldType': 'kpi', 'machineType': 'Diecast', 'fieldDisplayName': 'Quality'}, 'weight': 1, 'optimization_func': 'maximize'}, ...]
    "filters": {'duration': {'isEnabled': False, 'minimum': 0, 'unit': 'second'}, 'recordFilters': []},
    "dateRange": {'value': {'relativeAmount': 7, 'relativeUnit': 'day'}, 'config': {'mode': 'relative', 'selectableRelativeUnits': ['minute', 'hour', 'day', 'week', 'month', 'year'], 'enableTimeTypeSelection': True, 'showQuarterShortcuts': True}}
    "computeDeployedDateRange": None,
    "statsCalculationSetting": "defualt",
    "deployed":{recipe_group - deployed field}
 }
 ```

 ### id
 The id of the recipe group.

 ### values
 List of values that currently in the goup?

 ### runBoundaries
 List of constraints of boundaries?

 ### maxDuration
 This field is ignored by the system currently

 ### topRun
 The value of the topRun in this recipe group.

 ### constraints
 List of fields and values that are used to breakup runs They look like the following:
 ```
{
  "asset": "F1_010_BodyMaker_4",
  "name": "stats__BM 001: Cans Out__val",
  "type": "continuous",
  "values": [
    {
      "from": null,
      "from_is_inclusive": false,
      "to": 340,
      "to_is_inclusive": false
    },
    {
      "from": 340,
      "from_is_inclusive": true,
      "to": 6000,
      "to_is_inclusive": true
    },
    {
      "from": 6000,
      "from_is_inclusive": false,
      "to": null,
      "to_is_inclusive": false
    }
  ]
}
 ```
 #### asset
 The name of the asset the field used in the constraint.

 #### name
 The name of the field used for the constraint.

 #### type
 The data type of the constraint, mostly commonly continuous or categorical

 #### values
 These are the values to break up runs into.

 ### levers
 List of fields that go into recipe runs.  Looks like the following:
 ```
 {
    'fieldName': 'stats__AluminumTempAvg__val',
    'machineId': 'e2df2b4f115b763f45d04fa2',
    'machineName': 'JB_HM_Diecast_1',
    'machineDisplayName': 'Hamilton - Diecast 1',
    'fieldType': 'continuous',
    'machineType': 'Diecast',
    'fieldDisplayName': 'AluminumTemp - Average',
    'fieldUnit': 'celsius'
}
 ```
And here is a break down of each field:

#### fieldName
The name of field being looking.

#### machineId
The id of the machine this field belongs to.

#### machineName
The name of the machine this field belongs to.

#### machineDisplayName
The display name of the machine this field belongs to.

#### fieldType
What the type of the field is, commonly KPI, Continous or Categorical.

#### machineType
The machineType of the machine this field bleongs to.

#### fieldDisplayName
The display name of the field.

#### fieldUnit
The unit of the field.

### outcomes
A list of outcomes we are trying to optimize with this recipe_group:
```
{
    'field': 
    {
        'fieldName': 'quality',
        'machineId': 'e2df2b4f115b763f45d04fa2',
        'machineName': 'JB_HM_Diecast_1',
        'machineDisplayName': 'Hamilton - Diecast 1',
        'fieldType': 'kpi',
        'machineType': 'Diecast',
        'fieldDisplayName': 'Quality'
    },
    'weight': 1, 
    'optimization_func': 'maximize'
}
```
Here is more detail about each key:

#### field
The field you are trying to optimize with this outcome.  This is the same set up as [levers](#levers).

#### wieght
The wieght you are putting on this outcome as compared to the others.

#### optimization_func
How you wish to optimize this field usually 'maximize' or 'minize'

### filters
Object containing a duration filter and list of record filters
```
{'duration': {'isEnabled': False, 'minimum': 0, 'unit': 'second'}, 'recordFilters': []}
```

#### duration
This is the minimum run duration.

##### isEnabled
Whieter or not minimum run duration is enabled

##### minimum
The amount of time of what ever unit the minimum run duration is.

##### unit
The unit of time the minimum run duration uses.

#### recordFilters
List of record based filters.  They look like the following:
```
{
    asset: "F1_010_BodyMaker_4"
    name: "stats__0_BM: CPM__val"
    op: "gt"
    value: 1
}
```

##### asset
Name of the asset the field is on, usually a machine_name.

##### name
Name of the field.

##### op
The type of operation used to criteria match this filter.

##### value
The value of used for the criteria matching operation.

### dateRange
The date range that runs can look at.  Looks like this:
```
{
    'value': {
        'relativeAmount': 7,
        'relativeUnit': 'day'
    },
    'config': {
        ...
    }
}
```
Here is a breakdown of the keys:

#### value
The value of the dateRange. For relative config we have two keys, relativeAmount and relativeUnit.  This very similiar to [Data Viz time Selection](/docs/commonly_used_data_types/data_viz_query.md#time_selection).

##### relativeAmount
The amount of the relative range.

##### relativeUnit
The unit of the amount of the relative range.

#### config
This is used by the frontend UI and can be safely ignored for our purposes.

### statsCalculationSetting
How the recipe group runs calculations?  Can be set to defualt?

### deployed
The deployed version of this recipe_group.  It's a [recipe_group](#recipe_groups) minus this field.

## metadata
This is created by info, it includes the id of the user that created the cookbook along with their name and email

## updatetime
The time the cookbook was last updated.

## assets
A list of assets used in the cookbook?

## id
The id of the cookbook