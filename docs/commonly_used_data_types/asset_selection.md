# Asset Selection
Asset Selection is used in a few different places in order to tell the API which asset or assets you wish to perform an action on.  Typically it will either select a machine_type or types, or specific machines within a machine_type. In order to select machine_types it should look like the following:
```
asset_selection: {
    machine_type: ["Lasercut", ...]

}
```

In order to select machines within a type it should look like the following:
```
asset_selection: {
    machine_type: ["Lasercut"],
    machine_source: ["JB_AB_Lasercut_1", ...]

}
```

NOTE: The machine_type strings must match source_type, NOT source_type_clean.