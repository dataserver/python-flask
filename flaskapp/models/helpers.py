from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from flask import current_app as app

# from flaskapp.database import db


def iso_utc_to_tz(iso_utc_dt_str: str) -> str:
    """Formats a ISO-formatted UTC datetime string in the specified timezone and format.

    Args:
        iso_utc_dt_str (str): The input datetime string in ISO format with UTC timezone.
    Returns:
        str: Date string on format

    Examples:
        >>> app = {
        ...     "TIMEZONE": "America/Los_Angeles",
        ...     "DEFAULT_DISPLAY_DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S %Z"
        ... }
        >>> iso_utc_dt_str = "2023-04-18T12:05:00Z"
        >>> formatted_dt_str = filter_strftime(iso_utc_dt_str)
        >>> print(formatted_dt_str)  # Output: 2023-04-18 05:05:00 Pacific Daylight Time
    """

    # Parse the UTC datetime string and set the timezone to UTC
    utc_dt = datetime.fromisoformat(iso_utc_dt_str).replace(tzinfo=ZoneInfo("UTC"))

    # Create the America/XYZ timezone object
    target_tz = ZoneInfo(app.config["TIMEZONE"])

    # Convert the UTC datetime object to America/XYZ timezone
    target_dt = utc_dt.astimezone(target_tz)

    return target_dt.strftime(app.config["DEFAULT_DISPLAY_DATETIME_FORMAT"])
