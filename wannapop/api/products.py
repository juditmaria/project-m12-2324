from flask import request, abort
from . import api_bp
from ..models import Product, db, Order, ConfirmedOrder
from .helper_json import json_response

@api_bp.route('/products', methods=['GET'])
def get_products():
    title_filter = request.args.get('title')

    if title_filter:
        products = Product.query.filter(Product.title.ilike(f'%{title_filter}%')).all()
    else:
        products = Product.query.all()

    # Convertir los productos en un formato JSONizable
    data = [{"id": product.id, "title": product.title, "description": product.description, "price": product.price} for product in products]
    return json_response(data)

@api_bp.route('/products/<int:id>', methods=['GET'])
def get_product_details(id):
    product = Product.query.get(id)

    if product is None:
        abort(404, f"El producto con ID {id} no fue encontrado")

    # Convertir el producto en un formato JSONizable
    data = {"id": product.id, "title": product.title, "description": product.description, "price": product.price}
    return json_response(data)

@api_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    if product is None:
        abort(404, f"El producto con ID {id} no fue encontrado")

    data = request.json  # Obtén los datos del cuerpo de la solicitud en formato JSON

    # Verificar si los datos están presentes antes de intentar acceder a ellos
    if data:
        # Actualiza los campos del producto si están presentes en los datos de la solicitud
        if 'title' in data:
            product.title = data['title']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = data['price']

        # Guarda los cambios en la base de datos
        db.session.commit()

    # Convierte el producto actualizado en un formato JSONizable y devuélvelo como respuesta
    updated_product = {
        "id": product.id,
        "title": product.title,
        "description": product.description,
        "price": product.price
    }

    return json_response(updated_product)

@api_bp.route('/products/<int:id>/orders', methods=['GET'])
def get_product_orders(id):
    product = Product.query.get(id)

    if product is None:
        abort(404, f"El producto con ID {id} no fue encontrado")

    # Consulta las órdenes asociadas con el producto específico
    orders = Order.query.filter_by(product_id=id).all()

    # Filtra las órdenes confirmadas
    confirmed_orders = [order for order in orders if ConfirmedOrder.query.filter_by(order_id=order.id).first()]

    # Convertir las órdenes en un formato JSONizable
    data = [{"id": order.id, "product_id": order.product_id, "offer": order.offer} for order in confirmed_orders]
    return json_response(data)
