from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Str(attribute="_id", dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    created_at = fields.DateTime(dump_only=True)

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class UserUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1))
    email = fields.Email()