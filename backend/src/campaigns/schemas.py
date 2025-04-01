from marshmallow import Schema, fields, validate
from datetime import datetime

class CampaignSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str()
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    budget = fields.Int()
    status = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    owner_id = fields.Int(required=True)

class CampaignUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=100))
    description = fields.Str()
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    budget = fields.Int()
    status = fields.Boolean()