import datetime as dt
import random
from typing import Any

from fastapi import FastAPI

import app.timezones

MORNING_ISO_TIME = "07:30"

morning = FastAPI()


@morning.get("/")
def root() -> str:
    """Greet the user good morning, whererver they may be."""
    location_data = get_random_location()
    return (
        f"It is currently {location_data['time']} in "
        + f"{location_data['location']}. Good morning, wherever you are! 🌞"
    )


@morning.get("/location")
def get_random_location(t: str = MORNING_ISO_TIME) -> dict[str, str]:
    """
    Get a random location name and the current time where it's currently closest
    to being morning.

    Accepts a parameter t, which is expected to be an ISO time string and has
    a default value of '08:00'.
    """
    tz_data = get_timezones(t)
    timezone_name = random.choice(tz_data["timezones"])
    _, location = timezone_name.split("/")
    return {"time": tz_data["time"], "location": location}


@morning.get("/timezones")
def get_timezones(t: str = MORNING_ISO_TIME) -> dict[str, Any]:
    """
    Get the timezones and the current time where it's currently closest to being
    morning.

    Accepts a parameter t, which is expected to be an ISO time string and has
    a default value of '08:00'.
    """
    morning_time = dt.time.fromisoformat(t)
    morning_offset = app.timezones.utc_offset(morning_time)
    offsets_map = app.timezones.utc_offsets_map()
    nearest_offset, timezone_names = app.timezones.nearest_to_offset(
        offsets_map, morning_offset
    )
    nearest_morning_time = dt.datetime.utcnow() + nearest_offset
    return {
        "time": nearest_morning_time.strftime("%H:%M"),
        "utc_offset": nearest_offset.total_seconds(),
        "timezones": timezone_names,
    }
