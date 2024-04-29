import pytest
from smsdk import client
from smsdk.utils import get_url
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
        cli.config["site.domain"] == "localnet"
    ), "Site domain should be set to localnet"

    tenant = "https://demo-sdk-test.localnet"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test", "Tenant should be initialized correctly"
    assert cli.config["protocol"] == "https", "Protocol should be set to HTTPS"
    assert (
        cli.config["site.domain"] == "localnet"
    ), "Site domain should be set to localnet"

    tenant = "http://demo-sdk-test.localnet:8080/"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test", "Tenant should be initialized correctly"
    assert cli.config["protocol"] == "http", "Protocol should be set to HTTP"
    assert (
        cli.config["site.domain"] == "localnet"
    ), "Site domain should be set to localnet"


def test_create_client_uri_special_cases() -> None:
    tenant = "://demo-sdk-test.localnet"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test", "Tenant should be initialized correctly"
    assert cli.config["protocol"] == "https", "Protocol should be set to HTTPS"
    assert (
        cli.config["site.domain"] == "localnet"
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
        cli.config["site.domain"] == "localnet"
    ), "Site domain should be set to localnet"

    tenant = "://demo-sdk-test.localnet:8080"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test", "Tenant should be initialized correctly"
    assert cli.config["protocol"] == "https", "Protocol should be set to HTTPS"
    assert (
        cli.config["site.domain"] == "localnet"
    ), "Site domain should be set to localnet"
