from flask import Flask
from flaskapp.blueprints import register_bps, register_errors_handlers
from flaskapp.config import config
from flaskapp.database import db
from flaskapp.extensions import init_extensions
from flaskapp.helpers import filter_strftime


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name or "default"))
    app.jinja_env.filters["strftime"] = filter_strftime

    # Register blueprints
    register_bps(app)
    register_errors_handlers(app)

    # Initialize Database
    db.init_app(app)

    # FlaskUUID, LoginManager
    init_extensions(app)

    return app
