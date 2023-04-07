def module_utility():
    """
    Function to register class functions as tool functions
    :return:
    """
    registry = {}

    def registrar(func):
        registry[func.__name__] = func
        return func  # normally a decorator returns a wrapped function,
        # but here we return func unmodified, after registering it

    registrar.all = registry
    return registrar


def get_url(protocol, tenant, site_domain):
    """
    Get the URL of the web address.

    :param protocol: The application layer protocol.
    :type protocol: :class:`string`
    :param tenant: The tenant name on the host.
    :type tenant: :class:`string`
    :param site_domain: The domain name of the URL.
    :type site_domain: :class:`string`
    """

    return "{}://{}.{}".format(protocol, tenant, site_domain)
