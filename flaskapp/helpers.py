from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from zoneinfo import ZoneInfo

from flask import Response
from flask import current_app as app


def filter_strftime(iso_utc_dt_str: str, format: str | None = None) -> str:
    """Formats a ISO-formatted UTC datetime string in the specified timezone and format.

    Args:
        iso_utc_dt_str (str): The input datetime string in ISO format with UTC timezone.
        format (str, optional): The output datetime format string.
        If not provided, the default display datetime format from the application's configuration is used.

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

    format = format if format else app.config["DEFAULT_DISPLAY_DATETIME_FORMAT"]
    return target_dt.strftime(format)


def listdirs(rootdir: str | Path):
    """
    Recursively lists all directories under the specified root directory.

    Args:
        rootdir (str or pathlib.Path): The root directory to start the search from.

    Returns:
        None: This function prints the directory paths to the console and does not return a value.

    Examples:
        >>> import pathlib
        >>> rootdir = pathlib.Path("/path/to/root/directory")
        >>> listdirs(rootdir)
        /path/to/root/directory/subdir1
        /path/to/root/directory/subdir2
        /path/to/root/directory/subdir3/subsubdir1
        /path/to/root/directory/subdir3/subsubdir2

    """
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
