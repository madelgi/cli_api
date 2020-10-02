"""
Resources for registering users.
"""
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

from .schema import user_post, user_get
from .service import UserService
from cli_api.common.errors import UserException
from cli_api.common.utils import get_bearer_token


api = Namespace(
    "Authentication",
    description="Endpoint for registering users, logging in/out, etc",
    path="/auth",
)


@api.route("/register")
class RegisterResource(Resource):
    @accepts(schema=user_post, api=api)
    def post(self):
        """
        Register a user to our service.
        """
        user = UserService.register_user(request.parsed_obj)
        return user_get.dump(user), 201


@api.route("/login")
class LoginResource(Resource):
    @accepts(schema=user_post, api=api)
    def post(self):
        """
        Log yourself in.
        """
        auth_token = UserService.login_user(request.parsed_obj)
        response_object = {
            "message": "Successfully logged in",
            "auth_token": auth_token.decode(),
        }

        return response_object, 200


@api.route("/logout")
class LogoutResource(Resource):
    def post(self):
        """
        Log yourself out.
        """
        auth_token = get_bearer_token()
        UserService.logout_user(auth_token)
        return {"message": "Successfully logged out", "auth_token": auth_token}, 200
