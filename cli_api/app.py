import os

from flask import Flask
from flask_restx import Api

from .extensions import db, bcrypt, migrate
from .config import config_by_name
from .common.errors import UserException, ServerException, handle_api_exception


def create_app(config_name: str):
    app = Flask(__name__)

    # App configuration from object
    app.config.from_object(config_by_name[config_name])

    # Register API routes
    register_routes(app)

    # Register error handlers
    register_error_handlers(app)

    # Register commands
    register_commands(app)

    # Add extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db=db)

    return app


def register_routes(app):
    from .script.controller import api as script_api
    from .auth.controller import api as auth_api

    api = Api(app, title="CLI API", version="0.1.0")
    api.add_namespace(script_api)
    api.add_namespace(auth_api)


def register_commands(app: Flask):
    from .commands import seed_db

    app.cli.add_command(seed_db)


def register_error_handlers(app: Flask):
    app.register_error_handler(ServerException, handle_api_exception)
    app.register_error_handler(UserException, handle_api_exception)
