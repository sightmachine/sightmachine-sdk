import typing
import re

ENCODING_MAP = {
    '.': '__',
    '_': '_5F',
    '5': '5',
    'F': 'F',
    '$': '_24',
    '2': '2',
    '4': '4',
}
ENCODING_RE = re.compile(r'_*_5F|_*_24|_*_\.__*|_*_\.|\.__*|___*|\$|\.')

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

def check_kw(kw: str) -> bool:
    print(f"type of kw is {type(kw)}")
    for key in [
        "machine_type", 
        "Machine",
        "machine__source", 
        "End Time",
        "endtime",
        "Start Time",
        "starttime"
    ]:
        if kw.startswith("_") or key in kw:
            return False
    return True

def escape_replacement(m):
    # type: (typing.Match) -> str
    return ''.join(map(ENCODING_MAP.__getitem__, m.group()))

def escape_mongo_field_name(field_name):
    # type: (str) -> str
    """
    Translation map for character encoding
    || Decoded   || Encoded     ||
    |    \.      |    __        |
    |    \._     |    ___5F     |
    |   _\._     | _5F___5F     |
    |   __+      | _5F(_5F)+    |
    |    _5F     |   _5F5F      |
    |   _+_5F    |  (_5F)+_5F5F |
    Note: underscore is only escaped if a leading or trailing character in name or multiple
    underscores are next to each other
    An encoding of _ => ___ ( _ x 3) does not work because it becomes impossible to decode _. (encoded _ x 5)
    See ma.tests.unit.utils.test_mongoutils.TestMongoEscapeUtils for test cases
    """
    return ENCODING_RE.sub(escape_replacement, field_name)