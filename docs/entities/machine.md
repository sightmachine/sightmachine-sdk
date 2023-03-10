# Machines
Machines are just that, machines in factories.  The machine object is how the Sight Machine software replesents and is the key to accessing data that we collect from them

## Functions

### get_type_from_machine
The get_type_from_machine function allows you to get the type of any machine from it's name and is called this way:
```
cli.get_type_from_machine(machine_name)
```

And will return something like the following:
```
'Lasercut'
```

### get_machine_schema
The get_machine_schema functions returns the fields of the machine schema for a given machine source and is called this way:
```
cli.get_machine_schema(machine_source, types, show_hidden, return_mtype)
```

The only required field in this case is the machine_source, we will go over each variable in a second.  The function will return a pandas data frame that looks like the following:
```
                            name                       display         type
0             stats__Alarms__val                        Alarms        float
1            stats__BLOCKED__val                       BLOCKED        float
2               stats__DOWN__val                          DOWN        float
3     stats__DefectCategory__val               Defect Category       string
```

#### machine_source
This is the name of the machine that you are trying to grab the schema of.  This is the only required parameter for this function.

#### types
This is an optional parameter and is a list of strings.  If this is set the function will only return colomns that match the types given.  For example if we were to pass ['string'] as our types parameter in the previous example we would instead have returned:
```
                            name                       display         type
0     stats__DefectCategory__val               Defect Category       string
```

#### show_hidden
This is an optional parameter and is a boolean.  There are a few fields we have set to be hiddden from our ui in our application and by defualt these are also hidden from the return in this function if set to True we will also return these fields.

#### return_mtype
This is an optional parameter and is a boolean. If set to True this will instead of returning just the pandas dataframe will return a Tupple with a string that is the machine type of the machine_soure for example:
```
('Lasercut',                             
                            name                       display         type
0             stats__Alarms__val                        Alarms        float
1            stats__BLOCKED__val                       BLOCKED        float
...)
```