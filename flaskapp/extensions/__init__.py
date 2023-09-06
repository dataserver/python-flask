import re
from http import HTTPStatus

from flask import abort, redirect, request, url_for
from flask_login import LoginManager
from flaskapp.database import db
from flaskapp.extensions.flask_uuid import FlaskUUID
from flaskapp.models import User


def init_extensions(app):
    flask_uuid = FlaskUUID()
    flask_uuid.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"  # type: ignore
    login_manager.session_protection = "strong"
    login_manager.login_message_category = "danger"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, user_id)

    @login_manager.unauthorized_handler
    def unauthorized():
        # if request.blueprint == "api_bps":
        if re.match(r"^(\/api\/)", request.path):
            abort(HTTPStatus.UNAUTHORIZED)
        return redirect(url_for("auth.login"))
