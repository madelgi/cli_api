from marshmallow import fields, Schema


class ScriptSchema(Schema):
    id = fields.Integer(attribute="id")
    user = fields.Integer(attribute="user")
    name = fields.String(attribute="name")
    content = fields.String(attribute="content")
    version = fields.Integer(attribute="version")


script_post = ScriptSchema(only=["name", "content"])
script_get = ScriptSchema()
