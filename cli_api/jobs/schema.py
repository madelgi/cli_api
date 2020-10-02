from marshmallow import fields, Schema


class JobSchema(Schema):
    id = fields.String(attribute="id")
    name = fields.String(attribute="name")
    submit_time = fields.DateTime(attribute="submit_time")
    complete_time = fields.DateTime(attribute="complete_time")
    description = fields.String(attribute="description")
    user_id = fields.Integer(attribute="user_id")
    complete = fields.Boolean(attribute="complete")
    results = fields.String(attribute="results")
