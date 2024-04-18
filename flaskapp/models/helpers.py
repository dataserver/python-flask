from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from flask import current_app as app

# from flaskapp.database import db


def utc_to_tz(utc_dt_str: str) -> str:
    """Convert string datetime, format: YYYY-MM-DD HH:MM:SS,
    to config timezone.

    Args:
        utc_dt_str (str): Datetime format:YYYY-MM-DD HH:MM:SS

    Returns:
        str: Date string on format YYYY-MM-DD HH:MM:SS
    """

    # Parse the UTC datetime string and set the timezone to UTC
    utc_dt = datetime.strptime(utc_dt_str, "%Y-%m-%d %H:%M:%S").replace(
        tzinfo=ZoneInfo("UTC")
    )

    # Create the America/XYZ timezone object
    target_tz = ZoneInfo(app.config["TIMEZONE"])

    # Convert the UTC datetime object to America/XYZ timezone
    target_dt = utc_dt.astimezone(target_tz)

    return target_dt.strftime("%Y-%m-%d %H:%M:%S")


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
