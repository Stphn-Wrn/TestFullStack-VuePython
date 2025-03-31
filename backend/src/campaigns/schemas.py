from marshmallow import Schema, fields, validate
from datetime import datetime
from src.users.schemas import UserSchema

class CampaignSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    description = fields.Str()
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    budget = fields.Int(validate=validate.Range(min=0))
    status = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    owner_id = fields.Int(required=True)
    
    owner = fields.Nested(UserSchema, dump_only=True)