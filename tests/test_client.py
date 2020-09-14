from __future__ import unicode_literals

from smsdk import client


def test_client_init():
    """ Test the client initialization. """

    cli = client.Client("demo")

    assert cli.tenant == "demo"
    assert cli.config["site.domain"] == "sightmachine.io"

    cli = client.Client("demo")

    # VERIFY
    assert cli.tenant == "demo"
    assert cli.config["site.domain"] == "sightmachine.io"
