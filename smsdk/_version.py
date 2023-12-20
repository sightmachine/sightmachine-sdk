#
"""
Track version information for sightmachine-sdk module here.
"""
import typing
import itertools
import requests
import warnings
import functools
import re


class VersionInfo(typing.NamedTuple):
    major: typing.Any
    minor: typing.Any
    patchlevel: typing.Any
    releaselevel: typing.Any
    serial: typing.Any

    def __str__(self) -> str:
        result = "".join(
            itertools.chain(
                ".".join(str(i) for i in self[:3] if i is not None),
                (str(i) for i in self[3:] if i is not None),
            )
        )
        return result


version_info = VersionInfo(1, 26, 0, "", None)
version = str(f"v{version_info}")


def sort_releases_descending(
    releases: typing.List[typing.Dict[str, typing.Any]]
) -> typing.List[typing.Dict[str, typing.Any]]:
    def version_key(
        release: typing.Dict[str, typing.Any]
    ) -> typing.Union[typing.Tuple[int, int, int, str], typing.Tuple[()]]:
        version = release["tag_name"]
        # Use regular expression to extract numerical and string parts
        match = re.match(r"(?i)v(\d+)\.(\d+)\.(\d+)(\D*)", version)
        if match:
            major, minor, patch, suffix = map(match.group, (1, 2, 3, 4))
            return int(major), int(minor), int(patch), suffix
        else:
            return ()

    return (
        sorted(releases, key=version_key, reverse=True)
        if len(releases) > 1
        else releases
    )


def get_latest_release_version(
    releases: typing.List[typing.Dict[str, typing.Any]]
) -> typing.Optional[typing.Any]:
    if releases:
        sorted_releases = sort_releases_descending(releases)
        return sorted_releases[0]["tag_name"]
    return None


def get_latest_sdk_release() -> typing.Optional[typing.Any]:
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # To raise an HTTPError for any bad responses
        releases = response.json()

        if releases:
            return get_latest_release_version(releases)
    except requests.RequestException as e:
        print(f"Error fetching latest SDK release: {e}")

    return None


class VersionCheckDecorator:
    api_version_printed = False

    @classmethod
    def version_check_decorator(cls, func: typing.Any) -> typing.Any:
        @functools.wraps(func)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            if not cls.api_version_printed:
                latest_sdk_release = get_latest_sdk_release()
                installed_sdk_release = version

                if (
                    installed_sdk_release is not None
                    and latest_sdk_release is not None
                    and latest_sdk_release != installed_sdk_release
                ):
                    warnings.warn(
                        f"Installed SDK Version: {installed_sdk_release}. "
                        f"It is recommended to install release version ({latest_sdk_release}).",
                        DeprecationWarning,
                    )
                cls.api_version_printed = True

            return func(*args, **kwargs)

        return wrapper


# Initialize the flag to False
api_version_printed = False

owner = "sightmachine"
repo = "sightmachine-sdk"
