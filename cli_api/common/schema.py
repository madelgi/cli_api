from marshmallow import Schema, fields


class ErrorSchema(Schema):
    """
    Helper class for wrapping a schema in a message/status. Useful for responses
    from post/put requests, etc.
    """
    status = fields.Integer()
    message = fields.String()
