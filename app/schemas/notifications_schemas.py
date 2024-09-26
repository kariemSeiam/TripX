from marshmallow import Schema, fields, validate

class NotificationSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    message = fields.Str(required=True)
    read = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    data = fields.Dict()

class MarkAsReadSchema(Schema):
    read = fields.Bool(required=True)
