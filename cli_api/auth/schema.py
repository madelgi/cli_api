from marshmallow import Schema

from cli_api.common.schema import MessageSchema


class UserSchema(Schema):
    """
    Schema for user object.
    """
    class Meta:
        fields = ("email", "registered_on", "admin", "password", "id")


user_post = MessageSchema(UserSchema(only=['email', 'password']))
user_get = UserSchema(only=['email', 'registered_on'])
user_debug = UserSchema()
