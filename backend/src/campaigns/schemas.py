from marshmallow import (
    Schema, 
    fields, 
    validate
)
from dateutil import parser
from datetime import datetime
class SafeDateTime(fields.DateTime):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, datetime):
            return value
        
        try:
            return parser.isoparse(value)
        except Exception:
            raise self.make_error("invalid", input=value)
        
class CampaignSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str()
    start_date = SafeDateTime(required=True)
    end_date = SafeDateTime(required=True)
    budget = fields.Int()
    status = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    owner_id = fields.Int(dump_only=True)

class CampaignUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=100))
    description = fields.Str()
    start_date = SafeDateTime(required=True)
    end_date = SafeDateTime(required=True)
    budget = fields.Int()
    status = fields.Boolean()
