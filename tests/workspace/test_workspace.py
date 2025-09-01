from smsdk.smsdk_entities.workspace.workspace import Workspace
from tests.conftest import TENANT

# Define all the constants used in the test
NUM_ROWS = 2
NUM_COL = 2
URL = "/api/workspace"

def test_get_utilities(get_session):
    workspace = Workspace(get_session, TENANT)

    # Run
    all_utilities = workspace.get_utilities(get_session)

    expected_list = ["get_utilities", "get_cycles"]

    assert len(all_utilities) == len(expected_list)
    assert all([a == b for a, b in zip(all_utilities, expected_list)])


def test_get_cycles(get_client):
    query = {
        "machine__source": "test_machine",
        "_only": ["cycle_id", "cycle_name"],
        "_limit": NUM_ROWS,
    }

    df = get_client.get_cycles(**query)

    assert df.shape
