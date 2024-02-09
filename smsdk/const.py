import os

API_KEY = os.environ.get("ENV_VAR_API_KEY")
API_SECRET = os.environ.get("ENV_VAR_API_SECRET")
TENANT = os.environ.get("ENV_VAR_TENANT")

# Check if any of the required environment variables are not set
if API_KEY is None or API_SECRET is None or TENANT is None:
    raise EnvironmentError("One or more required environment variables are not set.")
