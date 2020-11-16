import importlib
import pkgutil
from typing import Callable, Dict, Generic, List, NamedTuple, Set, Tuple, TypeVar


class MissingComponentError(ValueError):
    """Thrown when `Registry.get` fails because there was no component with the
    requested name.

    """

    pass


class MissingVersionError(ValueError):
    """Thrown when `Registry.get` fails because there was no component with the
    requested name and version, though a component with the requested name was
    found.

    """

    pass


class ComponentInfo(NamedTuple):
    name: str
    version: int


# Load components from top-level Python modules that begin with MODULE_PREFIX.
MODULE_PREFIX = "smsdk"
_initialized = False


def initialize() -> None:
    """Imports all subpackages of smsdk entites
    in order to trigger component registration.

    """
    global _initialized
    if _initialized:
        return

    for mod_info in pkgutil.iter_modules():
        if mod_info.name.startswith(MODULE_PREFIX):
            module = importlib.import_module(mod_info.name)
            module_path: List[str] = module.__path__  # type: ignore
            for pkg_info in pkgutil.walk_packages(module_path, module.__name__ + "."):
                importlib.import_module(pkg_info.name)

    _initialized = True


T = TypeVar("T", bound=type)


class Registry(Generic[T]):
    """Creates a registry for named subclasses of a given type.

    Each class in the registry is identified by a (name, version) pair.
    The version may be omitted; omitted versions are interpreted as version 1.

    """

    def __init__(self, base_class: T) -> None:
        """Creates a new Registry instance for subclasses of `base_class`."""
        self.base_class = base_class
        self._registered: Dict[Tuple[str, int], T] = {}
        self._components: Set[str] = set()

    def __repr__(self) -> str:
        return f"Registry({self.base_class})"

    def register(self, name: str, version: int = 1) -> Callable[[T], T]:
        """Registers a component class with a given name and version."""

        def decorator(cls: T) -> T:
            key = (name, version)
            existing = self._registered.get(key)
            if existing is not None:
                raise ValueError(f"{key} is already used for {existing!r}")
            if not issubclass(cls, self.base_class):
                raise TypeError(f"must be a subclass of {self.base_class!r}")
            self._registered[key] = cls
            self._components.add(name)
            return cls

        return decorator

    def get(self, name: str, version: int = 1) -> T:
        """Returns the class registered for the component named `name` with
        version `version`.

        :raises MissingComponentError: if there is no component registered with
            the name `name`.
        :raises MissingVersionError: if there is a component registered with the
            name `name`, but no component matches both `name` and `version`.

        """
        initialize()
        if name not in self._components:
            raise MissingComponentError(f'There is no entity named "{name}"')
        key = (name, version)
        if key not in self._registered:
            raise MissingVersionError(
                f'There is no entity named "{name}" version {version}'
            )
        return self._registered[key]

    def list(self) -> List[ComponentInfo]:
        """Returns a list of all registered component versions."""
        initialize()
        results = [ComponentInfo(name, ver) for name, ver in self._registered.keys()]
        return results
