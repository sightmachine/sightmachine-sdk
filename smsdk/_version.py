# _version.py

import typing as t_
import itertools


class VersionInfo(t_.NamedTuple):
    major: int
    minor: int
    patchlevel: int
    releaselevel: t_.Optional[str]
    serial: t_.Optional[int]

    def __str__(self) -> str:
        result = "".join(
            itertools.chain(
                ".".join(str(i) for i in self[:3] if i is not None),
                (str(i) for i in self[3:] if i is not None),
            )
        )
        return result


version_info = VersionInfo(1, 26, 0, "+dev", None)
version = str(f"v{version_info}")
