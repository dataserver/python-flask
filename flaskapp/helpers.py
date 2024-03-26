from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path

from flask import Response
from flask import current_app as app


def filter_strftime(value, format=None):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    dt = datetime.strptime(value, app.config["DEFAULT_DISPLAY_DATETIME_FORMAT"])
    ft = format if format else app.config["DATABASE_DATETIME_FORMAT"]
    return dt.strftime(ft)


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
