from abc import ABCMeta, abstractmethod
import enum

from typing import List, Dict, NamedTuple, Tuple, Union

from smsdk.register import Registry
import typing as t_


@enum.unique
class Level(enum.Enum):
    WARNING = "warning"
    ERROR = "error"


ConfigPath = Tuple[Union[int, str], ...]
ConfigPath.__doc__ = """\
A ConfigPath represents a path to an element in a hierarchy of dicts
and lists. An integer represents a 0-based offset into a list, while a string
represents a key in a dictionary. For example, given the structure

    {"a": [{"b": 1, "c": 2}, {"d": 3}], "e": 4}

the element at the ConfigPath ["a", 0, "c"] is 2, while the element at the
path ["e"] is 4.

"""


class ValidationMessage(NamedTuple):
    """Represents a message returned when validating a configuration.

    :ivar level: either Level.WARNING or Level.ERROR.
    :ivar path: ConfigPath indicating the object that this message applies to.
        For example, if the "asset" property of the first stream in a document
        had an issue then the path would be `["streams", 0, "asset"]`.
    :ivar message: message to present to the user.

    """

    level: Level
    path: ConfigPath
    message: str


class SmsdkEntities(metaclass=ABCMeta):
    component_type = "SmsdkEntities"

    @classmethod
    @abstractmethod
    # The subclasses of the SmsdkEntities class will be responsible
    # for defining their own __init__() methods, which will initialize
    # the session and base_url attributes.
    def __init__(self, session: t_.Any, base_url: str) -> None:
        # self.session = session
        # self.base_url = base_url
        pass


smsdkentities = Registry(SmsdkEntities)
