#
"""
Track version information for factorytx-core module here.
"""
import typing
import itertools
import requests
import warnings


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


def get_latest_sdk_release():
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    response = requests.get(api_url)

    if response.status_code == 200:
        releases = response.json()
        if releases:
            latest_release = releases[0]
            release_number = latest_release["tag_name"]
            return release_number
        else:
            return None
    else:
        return None


def check_version():
    # Define a global flag to track whether the API version has been printed
    global api_version_printed
    if not api_version_printed:
        latest_sdk_release = get_latest_sdk_release()
        installed_sdk_release = version

        if installed_sdk_release is not None:
            print(f"SDK Version: {installed_sdk_release}")

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


# Initialize the flag to False
api_version_printed = False

owner = "sightmachine"
repo = "sightmachine-sdk"
