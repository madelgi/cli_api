from marshmallow import fields, Schema

from .utils import get_placeholders


class ScriptSchema(Schema):
    id = fields.Integer(attribute="id")
    user = fields.Integer(attribute="user")
    name = fields.String(attribute="name")
    description = fields.String(attribute="description")
    content = fields.String(attribute="content")
    version = fields.Integer(attribute="version")
    placeholders = fields.Method("get_placeholders_from_content", attribute='placeholders')

    def get_placeholders_from_content(self, obj) -> dict:
        return get_placeholders(obj.content)


script_post = ScriptSchema(only=["name", "content", "description"])
script_get = ScriptSchema()
