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