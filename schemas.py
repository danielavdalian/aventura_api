from marshmallow import Schema, fields, validate

class FileSchema(Schema):
    file = fields.Field(required=True, type="file", description="Archivo a subir")
    custom_filename = fields.Str(description="Nombre custom del archivo")
    id = fields.Str(description="Id del Tributo")

class GetTributosSchema(Schema):

    id = fields.Int()
    name = fields.Str()
    district = fields.Int()
    total_points = fields.Int()
    img_src = fields.Str()

class PostTributosSchema(Schema):
    name = fields.Str()
    district = fields.Int()
    total_points = fields.Int()
    img_src = fields.Str()

class PutTributosSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required = False)
    district = fields.Int(required = False) 

class PuntosSchema(Schema):
    id = fields.Int(description="Id del tributo")
    puntos = fields.Int(description="Puntos a sumar")
    





