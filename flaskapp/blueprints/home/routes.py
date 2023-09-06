from flask import Response, make_response, render_template, send_from_directory
from flaskapp.blueprints.home import bp


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
