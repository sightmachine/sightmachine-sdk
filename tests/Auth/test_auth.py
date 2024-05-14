import pytest

from smsdk import client
from smsdk.utils import get_url
from mock import mock_open, MagicMock
from unittest.mock import patch


def test_auth_init():
    """Test that Authenticator host is set properly"""
    tenant = "demo-sdk-test"
    cli = client.Client(tenant)
    authed = cli.auth

    assert authed.host == get_url(
        cli.config["protocol"], tenant, cli.config["site.domain"], cli.config["port"]
    )


@patch("smsdk.ma_session.Session")
def test_auth__auth_basic_success(mocked):
    """Test that Authenticator can use basic auth"""

    class Response:
        ok = True
        text = "Success"

        @staticmethod
        def json():
            return []

    mocked.return_value = MagicMock(
        post=MagicMock(return_value=Response()), get=MagicMock(return_value=Response())
    )

    tenant = ""
    user = "usertest"
    passw = "test"
    cli = client.Client(tenant)
    authed = cli.auth

    assert authed._auth_basic(email=user, password=passw) is True
    mocked.return_value.post.assert_called_once_with(
        f"https://{tenant}.sightmachine.io/auth/password/login",
        data={"remember": "yes", "email": user, "username": user, "password": passw},
    )


@patch("smsdk.ma_session.Session")
def test_auth__auth_basic_failure(mocked):
    """
    Test that Authenticator can handle errors in basic auth.
    """

    class Response:
        ok = False
        text = "error"

        @staticmethod
        def json():
            return None

    mocked.return_value = MagicMock(
        post=MagicMock(return_value=Response()), get=MagicMock(return_value=Response())
    )

    tenant = "demo-sdk-test"
    user = "user@domain.com"
    passw = "password"
    cli = client.Client(tenant)
    authed = cli.auth

    with pytest.raises(RuntimeError):
        authed._auth_basic(email=user, password=passw)


@patch("smsdk.Auth.auth.Authenticator._auth_basic")
@patch("smsdk.Auth.auth.Authenticator._auth_apikey")
def test_auth_route_auth(mocked_apikey, mocked_basic):
    """
    Test that Authenticator can properly route to auth methods
    """
    tenant = "demo-sdk-test"
    user = "user@domain.com"
    passw = "password"

    secret_id = "1234466790dfsddfsd"
    key_id = "judhebd-5555-88i7-9bb2-a6baa6a97658"
    cli = client.Client(tenant)
    authed = cli.auth
    assert authed.login("basic", email=user, password=passw)
    mocked_basic.assert_called_once_with(email=user, password=passw)

    assert authed.login("apikey", secret_id=secret_id, key_id=key_id)
    mocked_apikey.assert_called_once_with(secret_id=secret_id, key_id=key_id)

    with pytest.raises(RuntimeError):
        authed.login("foo", extra="bar")


@patch("smsdk.ma_session.Session")
def test_auth__auth_apikey_success(mocked):
    """Test that Authenticator can use apikey auth"""

    class Response:
        ok = True
        text = "Success"
        status_code = 200

        @staticmethod
        def json():
            return {"results": []}

    mocked.return_value = MagicMock(
        post=MagicMock(return_value=Response()), get=MagicMock(return_value=Response())
    )

    tenant = ""
    secret_id = "secret_Test"
    key_id = "key_test"
    cli = client.Client(tenant)
    authed = cli.auth

    assert authed._auth_apikey(secret_id=secret_id, key_id=key_id) is True
    mocked.return_value.get.assert_called_once_with(
        f"https://{tenant}.sightmachine.io/v1/selector/assets",
        json={"limit": 50000, "db_mode": "sql"},
    )


@patch("smsdk.ma_session.Session")
def test_auth__auth_apikey_failure(mocked):
    """Test that Authenticator can handle errors in basic auth."""

    class Response:
        ok = False
        text = "error"

        @staticmethod
        def json():
            return None

    mocked.return_value = MagicMock(
        post=MagicMock(return_value=Response()), get=MagicMock(return_value=Response())
    )

    tenant = "demo-sdk-test"
    user = "user@domain.com"
    passw = "password"

    cli = client.Client(tenant)
    authed = cli.auth

    with pytest.raises(RuntimeError):
        authed._auth_basic(email=user, password=passw)


@patch("smsdk.ma_session.Session")
def test_auth_check_auth_success(mocked):
    """Test that Authenticator can properly determine if authed"""

    class Response:
        ok = True
        text = "Success"
        status_code = 200

        @staticmethod
        def json():
            return {"results": []}

    mocked.return_value = MagicMock(
        post=MagicMock(return_value=Response()), get=MagicMock(return_value=Response())
    )

    tenant = "demo-sdk-test"
    cli = client.Client(tenant)
    authed = cli.auth

    assert authed.check_auth() is True
    mocked.return_value.get.assert_called_once_with(
        f"https://{tenant}.sightmachine.io/v1/selector/assets",
        json={"limit": 50000, "db_mode": "sql"},
    )


# @patch("smsdk.ma_session.Session")
# def test_auth_check_auth_failure(mocked):
#     """Test that Authenticator can properly determine if authed"""

#     class Response:
#         ok = False
#         text = "error"

#         @staticmethod
#         def json():
#             return None

#     mocked.return_value = MagicMock(
#         post=MagicMock(return_value=Response()), get=MagicMock(return_value=Response())
#     )

#     tenant = "demo-sdk-test"
#     cli = client.Client(tenant)
#     authed = cli.auth

#     assert authed.check_auth() is False
#     mocked.return_value.get.assert_called_once_with(
#         f"https://{tenant}.sightmachine.io/api/cycle",
#         params={"_limit": 1, "_only": ["_id"]},
#     )

# Check Auth is currently broken might fix later
