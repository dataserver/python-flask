from datetime import datetime

import pytz
from flask import current_app as app

# from flaskapp.database import db


def now_local_time():
    return datetime.now(pytz.timezone(app.config["TIMEZONE"]))
