from flask import Response
from flask import current_app as app
from flask import (
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flaskapp.blueprints.home import bp
from flaskapp.models import User


@bp.route("/")
def index() -> Response:
    return make_response(
        render_template(
            "home/index.html",
            date={},
        )
    )


@bp.route("/robots.txt")
def static_from_root():
    return send_from_directory("static", "robots.txt")
