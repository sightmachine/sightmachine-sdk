import requests
import json
import warnings

from requests.utils import cookiejar_from_dict, default_headers

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from smsdk import config
from smsdk.utils import get_url
from smsdk.ma_session import MaSession

# # Load config for common api endpoints
ENDPOINTS = json.loads(pkg_resources.read_text(config, "api_endpoints.json"))
RESOURCE_CONFIG = json.loads(pkg_resources.read_text(config, "message_config.json"))
#
KEYWORDS = RESOURCE_CONFIG["keywords"]
SM_AUTH_HEADER_SECRET_ID = RESOURCE_CONFIG["auth_header-api-secret"]
SM_AUTH_HEADER_SECRET_ID_OLD = RESOURCE_CONFIG["auth_header-api-secret_old"]
SM_AUTH_HEADER_KEY_ID = RESOURCE_CONFIG["auth_header-api-key"]
X_SM_DB_SCHEMA = RESOURCE_CONFIG["x_sm_db_schema"]
X_SM_WORKSPACE_ID = RESOURCE_CONFIG["x_sm_workspace_id"]


class Authenticator(MaSession):
    """
    Provide access to multiple authentication methods of the platform. This class
    is not meant to be used outside of the Client object.
    """

    def __init__(self, client):
        """
        Initialize the authentication module.

        :param client: The Client object that will interface with the Auth module.
        :type client: :class:`Client`
        """
        super(Authenticator, self).__init__()

        # Setup session and store host
        self.requests = requests
        self.host = get_url(
            client.config["protocol"], client.tenant, client.config["site.domain"]
        )
        self.session.headers = default_headers()

    def _auth_basic(self, email=None, password=None):
        """
        Authenticate by sending email and password combo.

        :param email: The email associated with the user's account.
        :type email: :class:`string`
        :param password: The password associated with the user's account.
        :type password: :class:`string`
        """

        success = False
        if not email or not password:
            return success

        payload = {
            "username": email,
            "email": email,
            "password": password,
            "remember": "yes",
        }
        url = "{}{}".format(self.host, ENDPOINTS["Auth"]["url"])
        self.session.headers = default_headers()
        resp = self.session.post(url, data=payload)

        if not resp.ok:
            raise RuntimeError("Failed login attempt to {}.".format(url))
        elif KEYWORDS["KEYWORD_MISSING_ACCOUNT"] in resp.text:
            raise RuntimeError(
                "Failed login attempt to {}. Account not found.".format(url)
            )
        elif KEYWORDS["KEYWORD_INCORRECT_PASSWORD"] in resp.text:
            raise RuntimeError(
                "Failed login attempt to {}. Password does not match.".format(url)
            )
        elif KEYWORDS["KEYWORD_REQUIRES_SSO"] in resp.text:
            raise RuntimeError(
                "Failed login attempt to {}. Requires SSO authentication.".format(url)
            )
        else:
            success = True

        return success

    def _auth_apikey(self, secret_id, key_id):
        """
        Authenticate by sending an API key.

        :param key: The API key associated with the user's account.
        :type key: :class:`string`
        """
        success = False
        if not secret_id or not key_id:
            return success

        self.session.headers = self.get_json_headers()
        self.session.headers.update(
            {
                SM_AUTH_HEADER_SECRET_ID: secret_id,
                SM_AUTH_HEADER_SECRET_ID_OLD: secret_id,  # add v0/v1 compat
                SM_AUTH_HEADER_KEY_ID: key_id,
            }
        )
        if not self.check_auth():
            raise RuntimeError(
                "Failed login attempt to {}. Invalid secret or key".format(self.host)
            )
        else:
            success = True
        return success

    def login(self, method=None, **kwargs):
        """
        Authenticate to the client by passing a method and any protocol
        specific arguments.

        :param method: The protocol that will be used to authenticate with the server.
        :type method: :class:`string`
        """

        success = False
        if method == "basic":
            success = self._auth_basic(**kwargs)
        elif method == "apikey":
            success = self._auth_apikey(**kwargs)
        elif method is None:
            try:
                success = self._auth_apikey(**kwargs)
            except Exception:  # pylint:disable=broad-except
                warnings.warn("Could not auto-connect using `apikey` method")

            if success is False:
                try:
                    success = self._auth_basic(**kwargs)
                except Exception:  # pylint:disable=broad-except
                    warnings.warn("Could not auto-connect using `basic` method")

        else:
            raise RuntimeError("Invalid login method: {}".format(method))

        return success

    def logout(self):
        """
        Unauthenticate from the client and destroy credential cache.
        """

        try:
            self.session.cookies = cookiejar_from_dict({})
            self.session.headers = default_headers()
            return True
        except Exception:  # pylint:disable=broad-except
            return False

    def check_auth(self):
        """
        Determine if SDK has access to the client by checking the Cycle API.
        """
        try:
            url = "{}{}".format(self.host, ENDPOINTS["Cycle"]["alt_url"])
            resp = self._get_records(url, _limit=1, _only=["_id"])
            return isinstance(resp, list) and "error" not in resp
        except Exception:  # pylint:disable=broad-except
            return False
