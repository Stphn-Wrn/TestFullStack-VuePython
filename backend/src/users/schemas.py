import re
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime

def validate_username(username):
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        raise ValidationError("Le nom d'utilisateur ne peut contenir que des lettres, chiffres, tirets et underscores")

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=[validate.Length(min=3, max=50), validate_username])
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=6))
