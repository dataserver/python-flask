from http import HTTPStatus
from urllib.parse import urlparse
from uuid import UUID

from flask import abort
from flask import current_app as app
from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flaskapp.blueprints.admin import bp
from flaskapp.blueprints.admin.validators import UserEditForm, UserRegistrationForm
from flaskapp.database import db, literalquery
from flaskapp.exc import ErrorFormData, ErrorNotAdministrator
from flaskapp.models import User
from werkzeug.security import check_password_hash, generate_password_hash


@bp.route("/", methods=["GET"])
@login_required
def index():
    users = {}
    stmt = db.select(User).order_by(User.username)
    users = db.session.execute(stmt).scalars().all()
    return render_template(
        "admin/index.html",
        user_data={},
        users=users,
    )


@bp.route(
    "/users",
    methods=["GET"],
    strict_slashes=False,
)
@login_required
def users():
    try:
        if not current_user.is_admin:  # type: ignore
            raise ErrorNotAdministrator(
                "You do not have Administrator access",
                redirect_to=url_for("home.index"),
            )
        users = {}
        stmt = db.select(User).order_by(User.username)
        users = db.session.execute(stmt).scalars().all()
        return render_template(
            "admin/users.html",
            users=users,
        )
    except ErrorNotAdministrator as e:
        app.logger.debug(f"error {e.message}")
        app.logger.debug(e.errors)
        flash(
            message=e.message,
            category="error",
        )
    return redirect(url_for("admin.index"))


@bp.route("/user", methods=["POST", "GET"])
@login_required
def user_getpost():
    form = UserRegistrationForm(request.form)
    try:
        if not current_user.is_admin:  # type: ignore
            raise ErrorNotAdministrator(
                "You do not have Administrator access",
                redirect_to=url_for("home.index"),
            )

        if request.method == "POST":
            app.logger.debug(f"create New User")
            stmt = db.select(User).where(User.username == form.username.data)
            user = db.session.execute(stmt).scalar_one_or_none()
            if user:
                raise ErrorFormData("Username already being used")

            if not form.validate():
                raise ErrorFormData("Form error", errors={"form": form.errors})

            is_admin = True if form.is_admin.data == "1" else False
            user = User(
                username=form.username.data,
                password=generate_password_hash(password=form.password.data),
                is_admin=is_admin,
                display_name=form.display_name.data,
            )
            user.save()
            flash(
                message=f"User {form.username.data} added",
                category="success",
            )
            return redirect(url_for("admin.users"))
        # method GET
        return render_template(
            "admin/user_form.html",
            user_data={},
            form_action_url=url_for("admin.user_getpost"),
            form_method="post",
            form=form,
        )

    except (ErrorFormData, ErrorNotAdministrator) as e:
        app.logger.debug(f"error {e.message}")
        app.logger.debug(e.errors)
        flash(
            message=e.message,
            category="error",
        )
        if e.errors and "form" in e.errors:
            form = e.errors["form"]
            return render_template(
                "admin/user_form.html",
                user_data={
                    "username": form.username.data,
                    "is_admin": form.is_admin.data,
                    "display_name": form.display_name.data,
                },
                form_action_url=url_for("admin.user_getpost"),
                form=form,
                form_method="post",
            )
    abort(HTTPStatus.METHOD_NOT_ALLOWED)


#  unique_id is instance of uuid.UUID
#  convert a UUID to a string of hex digits in standard form
#  use str(unique_id))
@bp.route("/user/id/<uuid:unique_id>", methods=["GET"])
@login_required
def user_view(unique_id: UUID):
    app.logger.debug(f"request.method {request.method}")
    try:
        if not current_user.is_admin:  # type: ignore
            raise ErrorFormData("You do not have Administrator access")

        unique_id = str(unique_id)  # type: ignore
        form = UserEditForm(request.form)
        stmt = db.select(User).where(User.unique_id == unique_id)
        user = db.session.execute(stmt).scalar_one_or_none()
        if user is None:
            app.logger.debug(literalquery(stmt))
            raise ErrorFormData("User not found")

        return render_template(
            "admin/user_form.html",
            user_data=user,
            form_action_url=url_for("admin.user_put", unique_id=unique_id),
            form_method="put",
            form=form,
            next="",
        )
    except ErrorFormData as e:
        app.logger.debug(f"error {e.message}")
        app.logger.debug(e.errors)
        flash(
            message=e.message,
            category="error",
        )
    return redirect(url_for("admin.index"))


#  unique_id is instance of uuid.UUID
@bp.route("/user/id/<uuid:unique_id>", methods=["POST", "PUT"])
@login_required
def user_put(unique_id: UUID):
    app.logger.debug(f"request.method {request.method}")
    try:
        if not current_user.is_admin:  # type: ignore
            raise ErrorNotAdministrator("You do not have Administrator access")

        if unique_id is None:
            raise ErrorFormData("Unique ID is missing")

        unique_id = str(unique_id)  # type: ignore
        _method = request.form.get("_method")
        form = UserEditForm(request.form)

        app.logger.debug(f"unique_id {unique_id}")
        app.logger.debug(f"_method {_method}")
        app.logger.debug(f"update New User")

        if not form.validate():
            url = url_for("admin.user_view", unique_id=unique_id)
            raise ErrorFormData("Invalid Form", errors=form.errors, redirect_to=url)

        stmt = db.select(User).where(User.unique_id == unique_id)
        user = db.session.execute(stmt).scalar_one_or_none()
        if user is None:
            raise ErrorFormData("User not found")

        user.display_name = form.display_name.data
        if form.password.data != "":
            app.logger.debug(f"new password has being entered")
            user.password = generate_password_hash(
                password=generate_password_hash(password=form.password.data)
            )
        if user.unique_id != current_user.unique_id:  # type: ignore
            user.is_admin = True if form.is_admin.data == "1" else False

        user.save()
        app.logger.debug("commited")
        flash(
            message=f"{user.username}'s profile updated",
            category="success",
        )
    except (ErrorFormData, ErrorNotAdministrator) as e:
        app.logger.debug(f"error {e.message}")
        if e.errors:
            app.logger.debug(e.errors)
        flash(
            message="Invalid Form.",
            category="error",
        )
        if e.redirect_to:
            return redirect(e.redirect_to)
        else:
            return redirect(url_for("admin.index"))
    except Exception as e:
        db.session.rollback()
        flash(
            message="Operation failed",
            category="error",
        )

    return redirect(url_for("admin.index"))


#  unique_id is instance of uuid.UUID
@bp.route("/user/id/<uuid:unique_id>", methods=["DELETE"])
@login_required
def user_delete(unique_id: UUID):
    """Only accessible via javascript fetch"""
    try:
        if not current_user.is_admin:  # type: ignore
            raise ErrorNotAdministrator("You do not have Administrator access")

        if current_user.unique_id == unique_id:  # type: ignore
            raise ErrorFormData(
                "Target user is the current user: you cannot delete yourself"
            )

        unique_id = str(unique_id)  # type: ignore
        _method = request.form.get("_method")

        app.logger.debug(f"delete user {unique_id}")
        app.logger.debug(f"_method {_method}")

        stmt = db.select(User).where(User.unique_id == unique_id)
        user = db.session.execute(stmt).scalar_one_or_none()
        if user is None:
            raise ErrorFormData("User not found")

        db.session.delete(user)
        db.session.commit()
        app.logger.debug("commited")
        flash(
            message="User deleted",
            category="success",
        )
        json_reponse = {
            "message": f"User deleted",
            "url": url_for("admin.index"),
        }
        return jsonify(json_reponse)
    except (ErrorFormData, ErrorNotAdministrator) as e:
        app.logger.debug(f"error {e.message}")
        flash(
            message=e.message,
            category="error",
        )
        json_reponse = {
            "message": e.message,
            "url": url_for("admin.index"),
        }
        return jsonify(json_reponse)
