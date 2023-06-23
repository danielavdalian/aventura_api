from marshmallow import Schema, fields, validate

class FileSchema(Schema):
    file = fields.Field(required=True, type="file", description="Archivo a subir")
    custom_filename = fields.Str()
    id = fields.Str()

class GetTributosSchema(Schema):

    id = fields.Int()
    name = fields.Str()
    district = fields.Int()
    total_points = fields.Int()
    img_src = fields.Str()

class GetTributosIdSchema(Schema):
    id = fields.Int()

class PostTributosSchema(Schema):
    name = fields.Str()
    district = fields.Int()
    total_points = fields.Int()
    img_src = fields.Str()

class PuntosSchema(Schema):
    id = fields.Int()
    puntos = fields.Int()
    





