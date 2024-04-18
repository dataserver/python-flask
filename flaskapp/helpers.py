from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from zoneinfo import ZoneInfo

from flask import Response
from flask import current_app as app


def filter_strftime(utc_dt_str: str, format=None) -> str:
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

    format = format if format else app.config["DEFAULT_DISPLAY_DATETIME_FORMAT"]
    return target_dt.strftime(format)


def listdirs(rootdir):
    for path in Path(rootdir).iterdir():
        if path.is_dir():
            print(path)
            listdirs(path)


def docache(*, minutes=5, content_type="application/json; charset=utf-8"):
    """Flask decorator that allow to set Expire and Cache headers.

    Args:
        minutes (int, optional): duration of cache. Defaults to 5min
        content_type (str, optional): Mime-type. Defaults to "application/json; charset=utf-8".
    """

    def fwrap(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            r = f(*args, **kwargs)
            then = datetime.now() + timedelta(minutes=minutes)
            rsp = Response(r, content_type=content_type)
            rsp.headers.add("Expires", then.strftime("%a, %d %b %Y %H:%M:%S GMT"))
            rsp.headers.add("Cache-Control", "public,max-age=%d" % int(60 * minutes))
            return rsp

        return wrapped_f

    return fwrap
