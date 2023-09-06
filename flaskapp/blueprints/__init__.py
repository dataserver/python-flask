from flask import Flask
from flaskapp.blueprints.admin.routes import bp as admin_bp
from flaskapp.blueprints.auth.routes import bp as auth_bp
from flaskapp.blueprints.dashboard.routes import bp as dashboard_bp
from flaskapp.blueprints.home.routes import bp as home_bp

# example
# def bad_request(e):
#     """Bad request."""
#     return render_template("400.html"), 400
# def not_found(e):
#     """Page not found."""
#     if request.path.startswith("/abc/"):
#         # we return a custom blog 404 page
#         return render_template("abc/error/404.html"), 404
#     else:
#         return render_template("error404.html"), 404
# def method_not_allowed(e):
#     # if a request has the wrong method to our API
#     if request.path.startswith("/api/"):
#         return jsonify(error="Method Not Allowed"), 405
#     else:
#         return render_template("error/405.html"), 405
# def server_error(e):
#     """Internal server error."""
#     return render_template("error/500.html"), 500


def register_bps(app: Flask):
    """Register blueprints to app"""
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    # example
    # child = Blueprint("child", __name__, url_prefix="/child")
    # child.register_blueprint(abc_bp, url_prefix="/abc") # /child/abc
    # app.register_blueprint(child)


def register_errors_handlers(app: Flask):
    """
    Blueprint Error Handlers
    These error (404 and 405) handlers are only invoked from an appropriate raise
    statement or a call to abort in another of the blueprint's view functions
    """
    # example
    # app.register_error_handler(400, bad_request)
    # app.register_error_handler(404, not_found)
    # app.register_error_handler(405, method_not_allowed)
    # app.register_error_handler(500, server_error)
