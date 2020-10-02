from marshmallow import Schema, fields


class UserSchema(Schema):
    """
    Schema for user object.
    """
    email = fields.String(attribute="email")
    registered_on = fields.DateTime(attribute="registered_on")
    admin = fields.Boolean(attribute="admin")
    password = fields.String(attribute="password")
    id = fields.Integer(attribute="id")


user_post = UserSchema(only=["email", "password"])
user_get = UserSchema(only=["email", "registered_on"])
user_debug = UserSchema()
