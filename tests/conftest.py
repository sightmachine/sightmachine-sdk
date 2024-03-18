import os
from smsdk import client
from requests.sessions import Session
import pytest

API_KEY = os.environ.get("ENV_SDK_VAR_API_KEY")
API_SECRET = os.environ.get("ENV_SDK_VAR_API_SECRET")
TENANT = os.environ.get("ENV_SDK_VAR_TENANT")

# Check if any of the required environment variables are not set
if API_KEY is None or API_SECRET is None or TENANT is None:
    raise EnvironmentError("One or more required environment variables are not set.")


@pytest.fixture(scope="session")
def get_session():
    session = Session()
    return session


@pytest.fixture(scope="session")
def get_client():
    cli = client.Client(TENANT)
    cli.login("apikey", key_id=API_KEY, secret_id=API_SECRET)

    return cli
