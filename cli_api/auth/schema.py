from marshmallow import Schema


class UserSchema(Schema):
    """
    Schema for user object.
    """

    class Meta:
        fields = ("email", "registered_on", "admin", "password", "id")


user_post = UserSchema(only=["email", "password"])
user_get = UserSchema(only=["email", "registered_on"])
user_debug = UserSchema()
