from flask import current_app as app
from flask import render_template
from flask_login import current_user, login_required, login_user, logout_user
from flaskapp.blueprints.dashboard import bp


@bp.route("/")
@login_required
def index():
    return render_template(
        "dashboard/index.html",
    )
