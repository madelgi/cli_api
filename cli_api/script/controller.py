from flask import request
from flask_restx import Namespace, Resource


api = Namespace(
    'Script',
    description='Endpoint for adding, modifying, deleting various scripts',
    path='/scripts'
)


@api.route('/')
class ScriptResource(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass
