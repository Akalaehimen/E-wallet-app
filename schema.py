from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    surname = fields.Str(required=True)
    firstname = fields.Str(required=True)
    password = fields.Str(required=True)
    


class UsersSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class AirtimeSchema(Schema):
    id = fields.Int(dump_only=True)
    phone_number = fields.Int(required=True)
    amount = fields.Int(required=True)

class DataSchema(Schema):
    id = fields.Int(dump_only=True)
    phone_number = fields.Int(required=True)
    data_plan = fields.Str(required=True)

class CableSchema(Schema):
    id = fields.Int(dump_only=True)
    subscriber_number = fields.Int(required=True)
    package_name = fields.Str(required=True)

class ElectricitySchema(Schema):
    id = fields.Int(dump_only=True)
    provider = fields.Str(required=True)
    meter_number = fields.Int(required=True)
    amount = fields.Float(required=True)
    payment_mode = fields.Str(required=True)

class CryptoSchema(Schema):
    id = fields.Int(dump_only=True)
    number = fields.Str(required=True)

