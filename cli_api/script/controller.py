"""
Resources for the /scripts endpoint
"""
from flask import request
from flask_restx import Namespace, Resource
from flask_accepts import accepts, responds

from .schema import script_post, script_get
from .service import ScriptService
from cli_api.jobs.schema import JobSchema
from cli_api.auth.model import User
from cli_api.common.utils import get_bearer_token


api = Namespace(
    "Script",
    description="Endpoint for adding, modifying, deleting various scripts",
    path="/scripts",
)


@api.route("")
class ScriptResource(Resource):
    @responds(schema=script_get, api=api, status_code=200)
    def get(self):
        """
        Get all scripts.
        """
        auth_token = get_bearer_token()
        user_id = User.decode_auth_token(auth_token)
        return ScriptService.get_all_by_user(user_id)

    @accepts(schema=script_post, api=api)
    @responds(schema=script_get, api=api, status_code=201)
    def post(self):
        """
        Register a script with the backend.
        """
        auth_token = get_bearer_token()

        user_id = User.decode_auth_token(auth_token)
        script_obj = request.parsed_obj
        script_obj["user"] = user_id

        return ScriptService.create(script_obj)


@api.route("/<string:script_name>/execute")
class ScriptExecuteResource(Resource):

    @responds(schema=JobSchema)
    def post(self, script_name: int):
        auth_token = get_bearer_token()
        user_id = User.decode_auth_token(auth_token)
        return ScriptService.execute(user_id, script_name)
