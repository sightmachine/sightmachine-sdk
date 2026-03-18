import pytest
from smsdk import client
from tests.conftest import TENANT, API_SECRET, API_KEY


def test_basic_create_client_using_tenant() -> None:
    cli: client.Client = client.Client("")
    login_result = cli.login("apikey", key_id=API_KEY, secret_id=API_SECRET)

    assert login_result is False, "Login should fail"
    assert cli.tenant == "", "Tenant should be empty"
    assert cli.config["protocol"] == "https", "Protocol should be set to HTTPS"
    assert (
        cli.config["site.domain"] == "sightmachine.io"
    ), "Site domain should be set to sightmachine.io"

    tenant = ""
    if TENANT:
        tenant = TENANT
    cli = client.Client(tenant, protocol="http")
    login_result = cli.login("apikey", key_id=API_KEY, secret_id=API_SECRET)

    assert login_result is True, "Login should be successful"
    assert cli.tenant == tenant, "Tenant should be initialized correctly"
    assert cli.config["protocol"] == "http", "Protocol should be set to HTTP"
    assert (
        cli.config["site.domain"] == "sightmachine.io"
    ), "Site domain should be set to sightmachine.io"


def test_create_client_using_tenant() -> None:
    tenant = "demo"
    cli = client.Client(tenant)

    assert cli.tenant == "demo", "Tenant should be initialized correctly"
    assert cli.config["protocol"] == "https", "Protocol should be set to HTTPS"
    assert (
        cli.config["site.domain"] == "sightmachine.io"
    ), "Site domain should be set to sightmachine.io"

    cli = client.Client(tenant, protocol="http")

    assert cli.tenant == "demo", "Tenant should be initialized correctly"
    assert cli.config["protocol"] == "http", "Protocol should be set to HTTP"
    assert (
        cli.config["site.domain"] == "sightmachine.io"
    ), "Site domain should be set to sightmachine.io"

    cli = client.Client(tenant, site_domain="localnet")

    assert cli.tenant == "demo", "Tenant should be initialized correctly"
    assert cli.config["protocol"] == "https", "Protocol should be set to HTTPS"
    assert (
        cli.config["site.domain"] == "localnet"
    ), "Site domain should be set to localnet"


def test_create_client_using_uri() -> None:
    tenant = "demo-sdk-test.localnet"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test", "Tenant should be initialized correctly"
    assert cli.config["protocol"] == "https", "Protocol should be set to HTTPS"
    assert (
        cli.config["site.domain"] == "localnet.sightmachine.io"
    ), "Site domain should be set to localnet"

    tenant = "https://demo-sdk-test.localnet"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test", "Tenant should be initialized correctly"
    assert cli.config["protocol"] == "https", "Protocol should be set to HTTPS"
    assert (
        cli.config["site.domain"] == "localnet.sightmachine.io"
    ), "Site domain should be set to localnet"

    tenant = "http://demo-sdk-test.localnet:8080/"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test", "Tenant should be initialized correctly"
    assert cli.config["protocol"] == "http", "Protocol should be set to HTTP"
    assert (
        cli.config["site.domain"] == "localnet.sightmachine.io"
    ), "Site domain should be set to localnet"


def test_create_client_uri_special_cases() -> None:
    tenant = "://demo-sdk-test.localnet"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test", "Tenant should be initialized correctly"
    assert cli.config["protocol"] == "https", "Protocol should be set to HTTPS"
    assert (
        cli.config["site.domain"] == "localnet.sightmachine.io"
    ), "Site domain should be set to localnet"

    tenant = "http://demo-sdk-test"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test", "Tenant should be initialized correctly"
    assert cli.config["protocol"] == "http", "Protocol should be set to HTTP"
    assert (
        cli.config["site.domain"] == "sightmachine.io"
    ), "Site domain should be set to sightmachine.io"

    tenant = "demo-sdk-test.localnet:8080"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test", "Tenant should be initialized correctly"
    assert cli.config["protocol"] == "https", "Protocol should be set to HTTPS"
    assert (
        cli.config["site.domain"] == "localnet.sightmachine.io"
    ), "Site domain should be set to localnet"

    tenant = "://demo-sdk-test.localnet:8080"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test", "Tenant should be initialized correctly"
    assert cli.config["protocol"] == "https", "Protocol should be set to HTTPS"
    assert (
        cli.config["site.domain"] == "localnet.sightmachine.io"
    ), "Site domain should be set to localnet"


def test_create_client_with_explicit_base_path() -> None:
    """Test explicit base_path parameter"""
    tenant = "demo"
    cli = client.Client(tenant, base_path="/nested/one/two")

    assert cli.tenant == "demo", "Tenant should be initialized correctly"
    assert cli.config["base.path"] == "/nested/one/two", "Base path should be set"
    assert cli.config["protocol"] == "https", "Protocol should be set to HTTPS"
    assert (
        cli.config["site.domain"] == "sightmachine.io"
    ), "Site domain should be set to sightmachine.io"

    # Verify URL construction includes path
    from smsdk.utils import get_url

    url = get_url(
        cli.config["protocol"],
        cli.tenant,
        cli.config["site.domain"],
        cli.config["port"],
        cli.config.get("base.path"),
    )
    assert (
        url == "https://demo.sightmachine.io/nested/one/two"
    ), "URL should include nested path"


def test_create_client_with_url_including_path() -> None:
    """Test path extraction from tenant URL"""
    tenant = "https://demo.sightmachine.io/nested/one/two"
    cli = client.Client(tenant)

    assert cli.tenant == "demo", "Tenant should be extracted correctly"
    assert cli.config["base.path"] == "/nested/one/two", "Path should be extracted"
    assert cli.config["protocol"] == "https", "Protocol should be set to HTTPS"
    assert (
        cli.config["site.domain"] == "sightmachine.io"
    ), "Site domain should be set to sightmachine.io"

    # Verify URL construction includes path
    from smsdk.utils import get_url

    url = get_url(
        cli.config["protocol"],
        cli.tenant,
        cli.config["site.domain"],
        cli.config["port"],
        cli.config.get("base.path"),
    )
    assert (
        url == "https://demo.sightmachine.io/nested/one/two"
    ), "URL should include nested path"


def test_create_client_explicit_path_overrides_extracted() -> None:
    """Explicit base_path should override extracted path"""
    tenant = "https://demo.sightmachine.io/old/path"
    cli = client.Client(tenant, base_path="/new/path")

    assert cli.tenant == "demo", "Tenant should be extracted correctly"
    assert (
        cli.config["base.path"] == "/new/path"
    ), "Explicit path should override extracted path"
    assert cli.config["protocol"] == "https", "Protocol should be set to HTTPS"

    # Verify URL construction uses explicit path
    from smsdk.utils import get_url

    url = get_url(
        cli.config["protocol"],
        cli.tenant,
        cli.config["site.domain"],
        cli.config["port"],
        cli.config.get("base.path"),
    )
    assert (
        url == "https://demo.sightmachine.io/new/path"
    ), "URL should use explicit path"


def test_backward_compatibility_no_path() -> None:
    """Existing behavior without path should work unchanged"""
    tenant = "demo"
    cli = client.Client(tenant)

    assert cli.tenant == "demo", "Tenant should be initialized correctly"
    assert cli.config.get("base.path") is None, "Base path should be None by default"
    assert cli.config["protocol"] == "https", "Protocol should be set to HTTPS"
    assert (
        cli.config["site.domain"] == "sightmachine.io"
    ), "Site domain should be set to sightmachine.io"

    # Verify URL construction works without path
    from smsdk.utils import get_url

    url = get_url(
        cli.config["protocol"],
        cli.tenant,
        cli.config["site.domain"],
        cli.config["port"],
        cli.config.get("base.path"),
    )
    assert url == "https://demo.sightmachine.io", "URL should not include any path"


def test_create_client_with_path_and_port() -> None:
    """Test base_path with custom port"""
    tenant = "http://demo.sightmachine.io:8080/nested/path"
    cli = client.Client(tenant)

    assert cli.tenant == "demo", "Tenant should be extracted correctly"
    assert cli.config["base.path"] == "/nested/path", "Path should be extracted"
    assert cli.config["protocol"] == "http", "Protocol should be set to HTTP"
    assert cli.config["port"] == 8080, "Port should be set to 8080"
    assert (
        cli.config["site.domain"] == "sightmachine.io"
    ), "Site domain should be set to sightmachine.io"

    # Verify URL construction includes both port and path
    from smsdk.utils import get_url

    url = get_url(
        cli.config["protocol"],
        cli.tenant,
        cli.config["site.domain"],
        cli.config["port"],
        cli.config.get("base.path"),
    )
    assert (
        url == "http://demo.sightmachine.io:8080/nested/path"
    ), "URL should include port and path"


def test_create_client_with_trailing_slash_in_path() -> None:
    """Test that trailing slashes in paths are normalized"""
    tenant = "https://demo.sightmachine.io/nested/path/"
    cli = client.Client(tenant)

    assert cli.tenant == "demo", "Tenant should be extracted correctly"
    assert (
        cli.config["base.path"] == "/nested/path"
    ), "Trailing slash should be removed"

    # Verify URL construction normalizes path
    from smsdk.utils import get_url

    url = get_url(
        cli.config["protocol"],
        cli.tenant,
        cli.config["site.domain"],
        cli.config["port"],
        cli.config.get("base.path"),
    )
    assert (
        url == "https://demo.sightmachine.io/nested/path"
    ), "URL should have normalized path"
