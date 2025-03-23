from flask import Blueprint, jsonify, render_template, request
from sqlalchemy import func

from app.config.db import db
from app.controllers.schemas.productos import IngredienteSchema, ProductoSchema
from app.models.todo import Producto, Ingrediente, ProductoIngrediente
home_blueprint = Blueprint("home", __name__)


productos = [
    {
        'nombre': 'Helado de Chocolate Belga',
        'descripcion': 'Suave helado de chocolate belga con trozos de brownie',
        'precio': '$8.900',
        'imagen': 'https://images.unsplash.com/photo-1576186298776-3d0380f7e6ec?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80'
    },
    {
        'nombre': 'Fresa Clásica',
        'descripcion': 'Helado de fresa natural con trozos de fruta fresca',
        'precio': '$7.500',
        'imagen': 'https://images.unsplash.com/photo-1576506295286-5cda18df43e7?ixlib=rb-1.2.1&auto=format&fit=crop&w=1352&q=80'
    },
    {
        'nombre': 'Menta Chip',
        'descripcion': 'Helado de menta con chispas de chocolate negro',
        'precio': '$8.200',
        'imagen': 'https://images.unsplash.com/photo-1588195538326-c5b1e9f80a1c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80'
    }
]

@home_blueprint.route('/')
def inicio():
    return render_template('index.html', productos=productos)


# Helper para cálculos de productos
def calcular_metricas(producto_id):
    # Calcular las calorías totales del producto
    calorias = Producto.query.join(ProductoIngrediente).join(Ingrediente).filter(
        ProductoIngrediente.producto_id == producto_id
    ).with_entities(
        func.sum(Ingrediente.calorias_por_unidad * ProductoIngrediente.cantidad)
    ).scalar() or 0

    # Calcular el costo total del producto
    costo = Producto.query.join(ProductoIngrediente).join(Ingrediente).filter(
        ProductoIngrediente.producto_id == producto_id
    ).with_entities(
        func.sum(Ingrediente.precio * ProductoIngrediente.cantidad)
    ).scalar() or 0

    return calorias, costo


# Endpoints para Productos
@home_blueprint.route('/productos', methods=['GET'])
def obtener_productos():
    # Obtener todos los productos de la base de datos
    productos = Producto.query.all()

    # Crear una instancia del esquema
    schema = ProductoSchema(many=True)  

    # Serializar los productos usando el esquema
    productos_filtrados = schema.dump(productos)

    # Verificar si el parámetro 'html' está presente y es 'true'
    if request.args.get('html') == 'true':
        # Renderizar una plantilla HTML con los productos
        return render_template('index.html', productos=productos_filtrados)
    else:
        return jsonify(productos_filtrados)

@home_blueprint.route('/productos/<int:id>', methods=['GET'])
def get_producto(id):
    producto = Producto.query.get(id) 
    if producto:
        # Crear una instancia del esquema
        schema = ProductoSchema()  

        # Serializar los productos usando el esquema
        productos_filtrados = schema.dump(producto)

        return jsonify(productos_filtrados)

    else:
        return jsonify({'error': 'producto not found'}), 404
    

@home_blueprint.route('/productos_name', methods=['GET'])
def get_producto_by_name():

    # Obtener el parámetro 'nombre' de la consulta (query string)
    name = request.args.get('name')

    if not name:
        return jsonify({'error': 'El parámetro "name" es requerido'}), 400

    # Buscar el helado en la base de datos
    producto_name = Producto.query.filter_by(nombre=name).first()

    if producto_name:
        schema = ProductoSchema()  
        return jsonify(schema.dump(producto_name)), 200
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404


@home_blueprint.route('/productos/<int:id>/calorias', methods=['GET'])
def get_calorias(id):
    calorias, _ = calcular_metricas(id)
    return jsonify({'calorias': calorias})

@home_blueprint.route('/productos/<int:id>/rentabilidad', methods=['GET'])
def get_rentabilidad(id):
    producto = Producto.query.get_or_404(id)
    _, costo = calcular_metricas(id)
    return jsonify({'rentabilidad': producto.precio_venta - costo})

@home_blueprint.route('/productos/<int:id>/vender', methods=['PUT'])
def vender_producto(id):
    producto = Producto.query.get_or_404(id)
    if producto.cantidad_inventario < 1:
        return jsonify({'error': 'Inventario insuficiente'}), 400

    producto.cantidad_inventario -= 1

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({'error': 'No se pudo completar la transacción', 'detalle': str(e)}), 500


    return jsonify(ProductoSchema().dump(producto))


# Endpoints para Ingredientes
@home_blueprint.route('/ingredientes', methods=['GET'])
def get_ingredientes():

    ingredientes = Ingrediente.query.all()

    if ingredientes:

        schema = IngredienteSchema(many=True)  

        return jsonify(schema.dump(ingredientes))

    else:
        return jsonify({'error': 'No hay ingredientes'}), 404
    
@home_blueprint.route('/ingredientes/<int:id>', methods=['GET'])
def get_ingrediente_by_id(id):

    ingrediente = Ingrediente.query.get(id) 
    if ingrediente:
        # Crear una instancia del esquema
        schema = ProductoSchema()  

        # Serializar los productos usando el esquema
        productos_filtrados = schema.dump(ingrediente)

        return jsonify(productos_filtrados)

    else:
        return jsonify({'error': 'ingrediente not found'}), 404
    
@home_blueprint.route('/ingredientes_name', methods=['GET'])
def get_Ingrediente_by_name():

    # Obtener el parámetro 'nombre' de la consulta (query string)
    name = request.args.get('name')

    if not name:
        return jsonify({'error': 'El parámetro "name" es requerido'}), 400

    # Buscar el helado en la base de datos
    Ingrediente_name = Ingrediente.query.filter_by(nombre=name).first()

    if Ingrediente_name:
        schema = IngredienteSchema()  
        return jsonify(schema.dump(Ingrediente_name)), 200
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404


@home_blueprint.route('/ingredientes/<int:id>/es-sano', methods=['GET'])
def get_es_sano(id):
    ingrediente = Ingrediente.query.get_or_404(id)
    return jsonify({'es_sano': ingrediente.es_sano})

# Operaciones de inventario
@home_blueprint.route('/productos/<int:id>/reabastecer', methods=['PUT'])
def reabastecer_producto(id):
    producto = Producto.query.get_or_404(id)
    cantidad = request.json.get('cantidad', 1)
    producto.cantidad_inventario += cantidad
    db.session.commit()

    return jsonify(ProductoSchema().dump(producto))  

@home_blueprint.route('/productos/<int:id>/inventario', methods=['PUT'])
def renovar_inventario(id):
    producto = Producto.query.get_or_404(id)
    producto.cantidad_inventario = request.json['cantidad']
    db.session.commit()
    return  jsonify(ProductoSchema().dump(producto))  