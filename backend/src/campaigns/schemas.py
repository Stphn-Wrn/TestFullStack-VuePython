from marshmallow import Schema, fields, validate, ValidationError, validates
from datetime import datetime
from dateutil import parser

class SafeDateTime(fields.DateTime):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, datetime):
            return value
        try:
            return parser.isoparse(value)
        except (ValueError, AttributeError, TypeError) as error:
            raise self.make_error("invalid", input=value) from error

class CampaignSchema(Schema):
    class Meta:
        strict = True
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str()
    start_date = SafeDateTime(required=True)
    end_date = SafeDateTime(required=True)
    budget = fields.Decimal(places=2, validate=validate.Range(min=0))
    is_active = fields.Boolean(metadata={"description": "True=Active, False=Deactivated"})
    created_at = fields.DateTime(dump_only=True)
    owner_id = fields.Int(dump_only=True)

    @validates("end_date")
    def validate_end_date(self, value, **kwargs):
        if "start_date" in self.context and value <= self.context["start_date"]:
            raise ValidationError("end_date must be after start_date")

class CampaignUpdateSchema(Schema):
    class Meta:
        strict = True
    
    name = fields.Str(validate=validate.Length(min=1, max=100))
    description = fields.Str()
    start_date = SafeDateTime()
    end_date = SafeDateTime()
    budget = fields.Decimal(places=2, validate=validate.Range(min=0))
    is_active = fields.Boolean()
