"""
Resources for registering and logging in users.
"""
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

from .schema import user_post, user_get
from .service import UserService


api = Namespace(
    'Authentication',
    description='Endpoint for registering, logging in, etc',
    path='/auth'
)


@api.route('/register')
class RegisterResource(Resource):

    @accepts(schema=user_post, api=api)
    @responds(schema=user_get)
    def post(self):
        """
        Register a user to our service.
        """
        return UserService.register_user(request.parsed_obj)


@api.route('/login')
class LoginResource(Resource):

    @accepts(schema=user_post, api=api)
    @responds(schema=user_get)
    def post(self):
        pass



