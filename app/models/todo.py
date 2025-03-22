from app.config.db import db

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    precio_venta = db.Column(db.Float, nullable=False)
    cantidad_inventario = db.Column(db.Integer, default=0)
    imagen = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)

    # Relación con ProductoIngrediente
    ingredientes_asociados = db.relationship('ProductoIngrediente', back_populates='producto')

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    calorias_por_unidad = db.Column(db.Float, nullable=False)
    es_sano = db.Column(db.Boolean, default=False)

    # Relación con ProductoIngrediente
    productos_asociados = db.relationship('ProductoIngrediente', back_populates='ingrediente')

class ProductoIngrediente(db.Model):
    __tablename__ = 'producto_ingrediente'
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), primary_key=True)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), primary_key=True)
    cantidad = db.Column(db.Float, nullable=False)

    # Relaciones
    producto = db.relationship('Producto', back_populates='ingredientes_asociados')
    ingrediente = db.relationship('Ingrediente', back_populates='productos_asociados')