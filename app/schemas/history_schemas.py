from marshmallow import Schema, fields

class HistorySchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    trip_id = fields.Int()
    event_type = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime(dump_only=True)

class CreateHistorySchema(Schema):
    trip_id = fields.Int(required=True)
    event_type = fields.Str(required=True)
    description = fields.Str()
