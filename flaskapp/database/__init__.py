# from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flaskapp.database.literalquery import literalquery
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()
# ma = Marshmallow()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    SQLITE3 specific. Requires this query to respect foreign keys constrains.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
