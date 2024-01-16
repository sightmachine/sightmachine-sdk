# version_utils.py
"""
Utility functions to track version information for sightmachine-sdk module.
"""
import datetime
import typing as t_
import requests
import warnings
import functools
import re
from smsdk._version import version


class VersionCheckDecorator:
    api_version_printed = False
    last_version_check_time = None

    @classmethod
    def version_check_decorator(cls, func: t_.Any) -> t_.Any:
        @functools.wraps(func)
        def wrapper(*args: t_.Any, **kwargs: t_.Any) -> t_.Any:
            current_time = datetime.datetime.now()

            # Check if a week has passed since the last version check
            if cls.last_version_check_time is None or (
                current_time - cls.last_version_check_time > datetime.timedelta(days=7)
            ):
                cls.api_version_printed = False
                cls.last_version_check_time = current_time

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


def sort_releases_descending(
    releases: t_.List[t_.Dict[str, t_.Any]]
) -> t_.List[t_.Dict[str, t_.Any]]:
    def version_key(release: t_.Dict[str, t_.Any]) -> t_.List[t_.Union[int, str]]:
        return [
            (int(i) if i.isdigit() else i)
            for i in re.split(r"(\d+|\W+)", release["tag_name"].lower())
            if i
        ]

    return (
        sorted(releases, key=version_key, reverse=True)
        if len(releases) > 1
        else releases
    )


def get_latest_release_version(
    releases: t_.List[t_.Dict[str, t_.Any]]
) -> t_.Optional[t_.Any]:
    if releases:
        sorted_releases = sort_releases_descending(releases)
        return sorted_releases[0]["tag_name"]
    return None


def get_latest_sdk_release() -> t_.Optional[t_.Any]:
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


# Initialize the flag to False
api_version_printed = False
owner = "sightmachine"
repo = "sightmachine-sdk"

# Define version_check_decorator here
version_check_decorator = VersionCheckDecorator.version_check_decorator
