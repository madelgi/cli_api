from marshmallow import fields, Schema


class ScriptSchema(Schema):
    id = fields.Integer(attribute="id")
    user = fields.String(attribute="user")
    name = fields.String(attribute="name")
    content = fields.String(attribute="content")
    version = fields.Integer(attribute="version")
