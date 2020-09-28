import os

from flask import Flask
from flask_restx import Api

from .extensions import db, bcrypt
from .config import config_by_name


def create_app(config_name: str):
    app = Flask(__name__)

    # TODO app configuration
    app.config.from_object(config_by_name[config_name])

    # Register API routes
    register_routes(app)

    # Add extensions
    db.init_app(app)
    bcrypt.init_app(app)

    return app


def register_routes(app):
    from .script.controller import api as script_api
    from .auth.controller import api as auth_api

    api = Api(app, title="CLI API", version="0.1.0")
    api.add_namespace(script_api)
    api.add_namespace(auth_api)
