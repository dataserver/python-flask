from http import HTTPStatus
from urllib.parse import urlparse

from flask import abort
from flask import current_app as app
from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flaskapp.blueprints.auth import bp
from flaskapp.blueprints.auth.helpers import url_has_allowed_host_and_scheme
from flaskapp.blueprints.auth.validators import LoginForm
from flaskapp.database import db, literalquery
from flaskapp.exc import ErrorInvalidCredentials
from flaskapp.models import User
from werkzeug.security import check_password_hash, generate_password_hash


@bp.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            form = LoginForm(request.form)
            if not form.validate():
                raise ErrorInvalidCredentials(
                    "Credentials details are missing", errors=form.errors
                )

            next_page = form.next.data
            remember = True if form.remember.data == "1" else False

            stmt = db.select(User).where(User.username == form.username.data)
            user = db.session.execute(stmt).scalar_one_or_none()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user, remember=remember)
                host = urlparse(request.base_url)

                if next_page and url_has_allowed_host_and_scheme(
                    url=next_page, allowed_hosts=host.hostname
                ):
                    return redirect(next_page)
                else:
                    return redirect(url_for("dashboard.index"))
            else:
                raise ErrorInvalidCredentials("Credentials are wrong")

        # method GET
        next = request.args.get("next") if request.args.get("next") is not None else ""
        host = urlparse(request.base_url)
        if next and url_has_allowed_host_and_scheme(
            url=next, allowed_hosts=host.hostname
        ):
            next_page = next
        else:
            next_page = ""
        return render_template(
            "auth/login.html",
            next=next_page or "",
        )
    except ErrorInvalidCredentials as e:
        flash(message=e.message, category="error")
        print(e.errors)
        return redirect(url_for("auth.login"))


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash(message="You logout", category="success")
    return redirect(url_for("auth.login"))
