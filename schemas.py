from marshmallow import Schema, fields, validate


class GetTributosSchema(Schema):
    name = fields.Str()
    district = fields.Int()
    total_points = fields.Int()
    img_src = fields.Str()

class PostTributosSchema(Schema):
    name = fields.Str()
    district = fields.Int()
    total_points = fields.Int()
    img_src = fields.Str()


