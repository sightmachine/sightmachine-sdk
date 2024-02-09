from smsdk import client
from requests.sessions import Session
import pytest
from smsdk import const

# Define all the constants used in the test
# These values may change for each run.

API_KEY = const.API_KEY
API_SECRET = const.API_SECRET

TENANT = const.TENANT


@pytest.fixture(scope="session")
def get_session():
    session = Session()
    return session


@pytest.fixture(scope="session")
def get_client():
    cli = client.Client(TENANT)
    cli.login("apikey", key_id=API_KEY, secret_id=API_SECRET)

    return cli
