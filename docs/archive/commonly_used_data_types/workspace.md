# Workspace
Workspaces are different collections of Sight Machine Assets.  They can be used to store seprate sets of data.

## Using Workspace-id to access different workspaces
The Sightmachine SDK allows users to access data in different workspaces with the following function:
```
cli.select_workspace_id(workspace_id)
```

After running this funciton all future function calls will get you data from the selected workspace.