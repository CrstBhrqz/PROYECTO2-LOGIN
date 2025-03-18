from flask import Blueprint, render_template

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

