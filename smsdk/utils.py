import typing as t_
import functools
from typing import Any


class ModuleUtility:
    def __init__(self) -> None:
        self.registry: t_.Dict[str, t_.Callable[..., t_.Any]] = {}

    def __call__(self, func: t_.Callable[..., t_.Any]) -> t_.Callable[..., t_.Any]:
        self.registry[func.__name__] = func
        return func

    @property
    def all(self) -> t_.Dict[str, t_.Callable[..., t_.Any]]:
        return self.registry


# To avoid modifying all the files with the class name, this alias is created.
module_utility = ModuleUtility


def get_url(
    protocol: str, tenant: str, site_domain: str, port: t_.Optional[int] = None
) -> str:
    """
    Get the URL of the web address.

    :param protocol: The application layer protocol.
    :type protocol: :class:`string`
    :param tenant: The tenant name on the host.
    :type tenant: :class:`string`
    :param site_domain: The domain name of the URL.
    :type site_domain: :class:`string`
    :param port: The port number (defaults to None).
    :type port: :Int
    """

    url = ""

    if port is not None:
        url = f"{protocol}://{tenant}.{site_domain}:{port}"
    else:
        url = f"{protocol}://{tenant}.{site_domain}"

    return url
