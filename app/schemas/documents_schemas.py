from marshmallow import Schema, fields

class DocumentSchema(Schema):
    document_type = fields.Str(required=True)
    file = fields.Raw(required=True)

class DocumentStatusSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    document_type = fields.Str(dump_only=True)
    file_url = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
