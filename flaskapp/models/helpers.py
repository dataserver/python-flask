from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from flask import current_app as app

# from flaskapp.database import db


def iso_utc_to_tz(utc_dt_str: str) -> str:
    """Convert stored string datetime from database
    to format set in config timezone.

    Args:
        utc_dt_str (str): Datetime format

    Returns:
        str: Date string on format
    """

    # Parse the UTC datetime string and set the timezone to UTC
    utc_dt = datetime.fromisoformat(utc_dt_str).replace(tzinfo=ZoneInfo("UTC"))

    # Create the America/XYZ timezone object
    target_tz = ZoneInfo(app.config["TIMEZONE"])

    # Convert the UTC datetime object to America/XYZ timezone
    target_dt = utc_dt.astimezone(target_tz)

    return target_dt.strftime(app.config["DEFAULT_DISPLAY_DATETIME_FORMAT"])
