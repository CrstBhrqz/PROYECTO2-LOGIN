# Esquema para filtrar los datos del producto
from marshmallow import Schema, fields


class ProductoSchema(Schema):

    id = fields.Int()
    nombre = fields.Str()
    descripcion = fields.Str()
    imagen = fields.Str()
    precio = fields.Float(attribute="precio_venta")  # Cambia "precio_venta" a "precio"
