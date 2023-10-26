from smsdk import client
from requests.sessions import Session
import pytest


# Define all the constants used in the test
# These values may change for each run.
API_KEY = "cea8969e-2acd-4ff4-b88b-e6b62d5cd857"
API_SECRETE = "sma_nBy04LSDJhwxXNct8R8pREkwzbUTWjU4ZmQj7Y2ApAi_"

TENANT = "demo-sdk-test"


@pytest.fixture(scope="session")
def get_session():
    session = Session()
    return session


@pytest.fixture(scope="session")
def get_client():
    cli = client.Client(TENANT)
    cli.login("apikey", key_id=API_KEY, secret_id=API_SECRETE)

    return cli
