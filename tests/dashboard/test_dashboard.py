from smsdk.smsdk_entities.dashboard.dashboard import DashboardData
from tests.conftest import TENANT

URL = "/v1/obj/dashboard/"


def test_get_utilities(get_session):
    dashboard = DashboardData(get_session, TENANT)

    # Run
    all_utilities = dashboard.get_utilities(get_session, URL)

    expected_list = ["get_utilities", "get_dashboards"]

    assert len(all_utilities) == len(expected_list)
    assert all([a == b for a, b in zip(all_utilities, expected_list)])


def test_get_dashboards(get_client):
    dashboard_id = "test_dashboard"
    panels = get_client.get_dashboards(dashboard_id)
    # Assuming the test environment returns a list of panels
    assert isinstance(panels, list)
    if panels:
        assert "id" in panels[0]
