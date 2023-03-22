# Run
A recipe run or just run, is one set of inputs and outcomes for a cookbook recipe.  Runs look like the following:
```
{'_count': 12,
 '_count_muted': 0,
 '_duration_seconds': 649.0,
 '_earliest': '2022-10-21T00:35:32+00:00',
 '_latest': '2022-10-21T00:46:21+00:00',
 '_score': 1.0,
 'constraint_group_id': '0',
 'constraints': [],
 'cookbook': '63ab6b263fa4880c06334b03',
 'filters': [],
 'i_vals': [{'asset': 'SHARED', 'name': 'group', 'value': '0'},
            {'asset': 'SHARED', 'name': 'sequence', 'value': 2}],
 'levers': [{'asset': 'JB_HM_Diecast_1',
             'd_pos': 2,
             'name': 'stats__AluminumTempAvg__val',
             'value': {'avg': 659.8448127439334,
                       'count': 9.0,
                       'max': 671.1048565509,
                       'min': 653.718308813,
                       'var_pop': 29.816738449355437}},
            {'asset': 'JB_HM_Diecast_1',
             'd_pos': 3,
             'name': 'stats__AluminumTempMax__val',
             'value': {'avg': 659.8448127439334,
                       'count': 9.0,
                       'max': 671.1048565509,
                       'min': 653.718308813,
                       'var_pop': 29.816738449355437}},
            {'asset': 'JB_HM_Diecast_1',
             'd_pos': 4,
             'name': 'stats__DieTemp__val',
             'value': {'avg': 290.8228674053778,
                       'count': 9.0,
                       'max': 295.2332287849,
                       'min': 284.84446548529996,
                       'var_pop': 11.993829414162574}},
            {'asset': 'JB_HM_Diecast_1',
             'd_pos': 5,
             'name': 'stats__InjectionCurveDifference__val',
             'value': {'avg': 1.576386980588889,
                       'count': 9.0,
                       'max': 2.8598220936,
                       'min': 0.3786822327000001,
                       'var_pop': 0.810658290414194}},
            {'asset': 'JB_HM_Diecast_1',
             'd_pos': 6,
             'name': 'stats__InjectionPressureMax__val',
             'value': {'avg': 39.537370569911104,
                       'count': 9.0,
                       'max': 44.0884060904,
                       'min': 35.4952094968,
                       'var_pop': 5.452849234986407}},
            {'asset': 'JB_HM_Diecast_1',
             'd_pos': 7,
             'name': 'stats__InjectionPressureMin__val',
             'value': {'avg': 36.76283137485556,
                       'count': 9.0,
                       'max': 38.8721003798,
                       'min': 35.0169147198,
                       'var_pop': 1.2194962602188073}}],
 'outcomes': [{'asset': 'JB_HM_Diecast_1',
               'd_pos': 0,
               'kpi': {'aggregates': {'Output': 'sum', 'ScrapQuantity': 'sum'},
                       'dependencies': {'Output': 9.0, 'ScrapQuantity': 0.0},
                       'formula': '((Output) / (Output + ScrapQuantity)) * 100 '
                                  'if ((Output + ScrapQuantity) > 0) else '
                                  'None'},
               'name': 'quality',
               'value': {'avg': 100.0,
                         'count': 100.0,
                         'max': 100.0,
                         'min': 100.0,
                         'normal': 1.0000000000000002,
                         'var_pop': 100.0}}]}
```

We will go over each key in more detail

## _count
The number of total records in the run.

## _count_muted
The number of records filtered out in the run.

## _duration_seconds
The duration of the run in  seconds.

## _earliest
The start time of the run.

## _latest
The end time of the run.

## _score
The 'score' this run achieved.

## constraint_group_id
The id of the group of constraints in the cookbook.

## constraints
A list of the constraints on this run.

## cookbook
The id of the cookbook this run relates to.

## filters
A list of filters on this run.

## i_vals
Lists the constraint and/or run boundary values that were used to delimit this run.

## levers
A list of the levers attached to this run and their values.  A lever is in this format:
```
{
'asset': 'JB_HM_Diecast_1',
'd_pos': 2,
'name': 'stats__AluminumTempAvg__val',
'value': {
        'avg': 659.8448127439334,
        'count': 9.0,
        'max': 671.1048565509,
        'min': 653.718308813,
        'var_pop': 29.816738449355437
    }
}
```

### asset
The name of asset this lever is on, this is a machine_name

### d_pos
The index of the corresponding dependent variable in the linevis query. Internal use only.

### name
The actual name of the field being looked at.

### value
The values that this lever was measured at during this run.  It is futher broken down into the following keys.

#### avg
Average value during the run.

#### count
The amount of records during the run.

#### max
The maxium value recorded during the run.

#### min
The minimum value recorded during the run.

#### var_pop
Population variance.

## outcomes
A list of outcomes recorded during the run.  It looks like:
```
{
    'asset': 'JB_HM_Diecast_1',
    'd_pos': 0,
    'kpi': {
        'aggregates': {'Output': 'sum', 'ScrapQuantity': 'sum'},
        'dependencies': {'Output': 9.0, 'ScrapQuantity': 0.0},
        'formula': '((Output) / (Output + ScrapQuantity)) * 100 '
                    'if ((Output + ScrapQuantity) > 0) else '
                    'None'
    },
    'name': 'quality',
    'value': {
        'avg': 100.0,
        'count': 100.0,
        'max': 100.0,
        'min': 100.0,
        'normal': 1.0000000000000002,
        'var_pop': 100.0
    }
}
```

### asset
The name of the asset that outcome is attached to.  Usually a machine name.

### d_pos
The index of the corresponding dependent variable in the linevis query. Internal use only.

### kpi
If the outcome is a kpi this field will descripe the kpi.  It has the following keys:

#### aggregates
How we aggregate each field being feed into our kpi formula, can be sum, avg, min or max.

#### dependencies
The variables in the KPI formula.

#### formula
The actual formula the kpi uses

### name
The name of the field that the outcome is being tracked from.

### value
The values that this outcome was measured at during this run.  It is futher broken down into the following keys.

#### avg
Average value during the run.

#### count
The amount of measurements during the run.

#### max
The maxium value recorded during the run.

#### min
The minimum value recorded during the run.

#### normal
A measure of the normal distribution of the values recorded during the run
