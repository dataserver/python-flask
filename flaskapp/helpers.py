from datetime import datetime
from pathlib import Path

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
