import logging
import secrets

from werkzeug.security import generate_password_hash


class Config(object):
    AUTHENTICATING_HTTP = False
    DEBUG = True
    LOGGING_LEVEL = logging.WARNING
    SECRET_KEY = secrets.token_hex()

    RESULTS_LIMIT = 10

    SWAGGER_SPECIFICATION_DIR = "."
    SWAGGER_SPECIFICATION = "swagger.yml"

    USERS = dict()

    @staticmethod
    def init_app(app):
        file_handler = logging.StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class DevelopmentConfig(Config):
    AUTHENTICATING_HTTP = True
    LOGGING_LEVEL = logging.INFO

    USERS = dict(
        test=generate_password_hash("password"),
    )


class ProductionConfig(Config):
    AUTHENTICATING_HTTP = True


configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
