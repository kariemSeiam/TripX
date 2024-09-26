from marshmallow import Schema, fields

class RatingSchema(Schema):
    id = fields.Int(dump_only=True)
    driver_id = fields.Int()
    rider_id = fields.Int()
    trip_id = fields.Int()
    rating = fields.Float()
    feedback = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class CreateRatingSchema(Schema):
    driver_id = fields.Int(required=True)
    trip_id = fields.Int(required=True)
    rating = fields.Float(required=True)
    feedback = fields.Str()
