from pathlib import Path


class Config(object):
    DEBUG = False
    LOGIN_DISABLED = False
    #  $ python -c "import secrets; print(secrets.token_hex())"
    SECRET_KEY = "32d205291ea382c61a0e57ed34c92f66bd500758b1a34716b2ba168a6367bb17"
    TIMEZONE = "America/Sao_Paulo"
    DEFAULT_DISPLAY_DATETIME_FORMAT = "%Y-%m-%d %H:%M"


class ProdConfig(Config):
    DEBUG = False
    BASE_PATH = "/home/user/project/flaskapp"
    DATABASE_PATH = "/home/user/project/flaskapp/database/database.sqlite3"

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"


class DevConfig(Config):
    # flask
    DEBUG = True
    TESTING = True
    EXPLAIN_TEMPLATE_LOADING = False

    # flask-login
    LOGIN_DISABLED = False

    BASE_PATH = "d:/python/boilerplates/python-flask/flaskapp"
    DATABASE_PATH = Path(
        "d:/python/boilerplates/python-flask/flaskapp/database", "dev.sqlite3"
    )

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{str(DATABASE_PATH)}"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


config = {
    "dev": DevConfig,
    "production": ProdConfig,
    "default": DevConfig,
}
