import datetime as dt
import zoneinfo
from collections import defaultdict

EXCLUDED_TIMEZONE_NAMES = {"GMT", "UTC", "UCT", "Universal"}


def utc_offset(time: dt.time) -> dt.timedelta:
    """Get the UTC offset towards a given local time."""
    now = dt.datetime.now().astimezone()
    target = dt.datetime.combine(dt.date.today(), time).astimezone()
    local_offset = now.utcoffset()
    if local_offset is None:
        raise ValueError("Unable to get the UTC offset for the current timezone")
    return target - now + local_offset


def utc_offsets_map() -> dict[dt.timedelta, list[str]]:
    """
    Construct a look-up table mapping current UTC offsets for all interesting
    timezones into lists with timezone names having that UTC offset.
    """
    lookup = defaultdict(list)
    for timezone_name in _timezone_names():
        utc_offset = _current_utc_offset(timezone_name)
        lookup[utc_offset].append(timezone_name)
    return lookup


def nearest_to_offset(
    utc_offsets_map: dict[dt.timedelta, list[str]], offset: dt.timedelta
) -> tuple[dt.timedelta, list[str]]:
    """
    Return a pair with the nearest timedelta to a given offset and the
    timezones under that nearest timedelta in the offsets map.
    """
    return min(
        utc_offsets_map.items(),
        key=lambda entry: abs(offset.total_seconds() - entry[0].total_seconds()),
    )


def _timezone_names() -> list[str]:
    """
    Get all available timezone names on the form 'Region/Location' that do not
    match any of the EXCLUDED_TIMEZONE_NAMES.
    """

    def _is_locational_name(timezone_name: str) -> bool:
        parts = timezone_name.split("/")
        if not len(parts) == 2:
            return False

        _, location = parts
        return (
            location.isalpha()
        )  # isalpha will remove any "location" with numbers, e.g. GMT+0

    def _should_not_be_excluded(timezone_name: str) -> bool:
        return not any(
            excluded in timezone_name for excluded in EXCLUDED_TIMEZONE_NAMES
        )

    return [
        timezone_name
        for timezone_name in zoneinfo.available_timezones()
        if _is_locational_name(timezone_name) and _should_not_be_excluded(timezone_name)
    ]


def _current_utc_offset(timezone_name: str) -> dt.timedelta:
    maybe_offset = dt.datetime.now(zoneinfo.ZoneInfo(timezone_name)).utcoffset()
    if maybe_offset is None:
        raise ValueError(
            f"Unable to get current UTC offset for timezone: {timezone_name}"
        )
    return maybe_offset
