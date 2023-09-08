# Common SDK Errors

## Not Found
ValueError: Error - {"description":"The requested page or resource was not found","details":{},"error":"not_found"}

#### Potential Causes
- This error can occur if there's no data available for the time you queried.


## Server Error
ValueError: Error - {"description":"An unexpected error occurred.","details":{},"error":"server_error"}

#### Potential Causes
- This error can occur if there is a weird SDK bug, such as not being able to handle all-numeric machine names. 
- Sometimes you may see this error but the SDK will still return the expected data.
