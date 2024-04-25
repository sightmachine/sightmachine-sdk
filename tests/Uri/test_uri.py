import pytest
from smsdk import client
from smsdk.utils import get_url


def test_create_client_using_tenant() -> None:
    tenant: str = ""
    cli: client.Client = client.Client(tenant)

    assert cli.tenant == tenant
    assert cli.config["protocol"] == "https"
    assert cli.config["site.domain"] == "sightmachine.io"

    tenant = "demo"
    cli = client.Client(tenant)

    assert cli.tenant == "demo"
    assert cli.config["protocol"] == "https"
    assert cli.config["site.domain"] == "sightmachine.io"

    cli = client.Client(tenant, protocol="http")

    assert cli.tenant == "demo"
    assert cli.config["protocol"] == "http"
    assert cli.config["site.domain"] == "sightmachine.io"

    cli = client.Client(tenant, site_domain="localnet")

    assert cli.tenant == "demo"
    assert cli.config["protocol"] == "https"
    assert cli.config["site.domain"] == "localnet"


def test_create_client_using_uri() -> None:
    tenant = "demo-sdk-test.localnet"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test"
    assert cli.config["protocol"] == "https"
    assert cli.config["site.domain"] == "localnet"

    tenant = "https://demo-sdk-test.localnet"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test"
    assert cli.config["protocol"] == "https"
    assert cli.config["site.domain"] == "localnet"

    tenant = "http://demo-sdk-test.localnet:8080/"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test"
    assert cli.config["protocol"] == "http"
    assert cli.config["site.domain"] == "localnet"


def test_create_client_uri_special_cases() -> None:
    tenant = "://demo-sdk-test.localnet"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test"
    assert cli.config["protocol"] == "https"
    assert cli.config["site.domain"] == "localnet"

    tenant = "http://demo-sdk-test"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test"
    assert cli.config["protocol"] == "http"
    assert cli.config["site.domain"] == "sightmachine.io"

    tenant = "demo-sdk-test.localnet:8080"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test"
    assert cli.config["protocol"] == "https"
    assert cli.config["site.domain"] == "localnet"

    tenant = "://demo-sdk-test.localnet:8080"
    cli = client.Client(tenant)

    assert cli.tenant == "demo-sdk-test"
    assert cli.config["protocol"] == "https"
    assert cli.config["site.domain"] == "localnet"
