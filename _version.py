#
"""
Track version information for factorytx-core module here.
"""
import typing
import itertools
import requests
import warnings
import functools


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


def get_latest_sdk_release() -> typing.Optional[typing.Any]:
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"

    try:
        response = requests.get(api_url)

        # To raise an HTTPError for any bad responses
        response.raise_for_status()

        releases = response.json()
        if releases:
            latest_release = releases[0]
            return latest_release["tag_name"]
    except requests.RequestException as e:
        print(f"Error fetching latest SDK release: {e}")

    return None


def version_check_decorator(func: typing.Any) -> typing.Any:
    @functools.wraps(func)
    def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        # Define a global flag to track whether the API version has been printed
        global api_version_printed
        if not api_version_printed:
            latest_sdk_release = get_latest_sdk_release()
            installed_sdk_release = version

            if (
                installed_sdk_release is not None
                and latest_sdk_release is not None
                and latest_sdk_release != installed_sdk_release
            ):
                warnings.warn(
                    f"Installed SDK Version: {installed_sdk_release}. It is recommended to install release version ({latest_sdk_release}).",
                    DeprecationWarning,
                )
            # Set the flag to True to indicate that the version has been printed
            api_version_printed = True

        return func(*args, **kwargs)

    return wrapper


# Initialize the flag to False
api_version_printed = False

owner = "sightmachine"
repo = "sightmachine-sdk"
