from marshmallow import Schema, fields


class MessageSchema(Schema):
    """
    Helper class for wrapping a schema in a message/status. Useful for responses
    from post/put requests, etc.
    """
    ok = fields.Boolean()
    message = fields.String()

    def __init__(self, schema: Schema = None):
        print(self.fields)
        if schema:
            self.fields["data"] = schema.fields
