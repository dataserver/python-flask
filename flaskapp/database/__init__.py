# from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    https://www.sqlite.org/foreignkeys.html
    2. Enabling Foreign Key Support
    Foreign key constraints are disabled by default

    SQLITE3 specific. Requires this query to respect foreign keys constrains.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
