from smsdk import client
from requests.sessions import Session
import pytest


# Define all the constants used in the test
# These values may change for each run.
API_KEY = "5a73aa5a-1962-4df9-b56e-4a59462f0f00"
API_SECRETE = "sma_FajgH3VbPu68gwy0PzccvhyGRyy1a8CCHhhvy6ooeg1O_"

TENANT = "demo"


@pytest.fixture(scope="session")
def get_session():
    session = Session()
    return session


@pytest.fixture(scope="session")
def get_client():
    cli = client.Client(TENANT)
    cli.login("apikey", key_id=API_KEY, secret_id=API_SECRETE)

    return cli