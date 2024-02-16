from flask import abort
from . import api_bp
from ..models import Order, ConfirmedOrder, db

@api_bp.route('/orders/<int:id>/confirmed', methods=['POST'])
def accept_offer(id):
    order = Order.query.get(id)

    if order is None:
        abort(404, f"La oferta con ID {id} no fue encontrada")

    # Crea una entrada en la tabla de órdenes confirmadas
    confirmed_order = ConfirmedOrder(order_id=id)
    db.session.add(confirmed_order)
    db.session.commit()

    return {'message': f'Oferta con ID {id} aceptada correctamente'}, 200

@api_bp.route('/orders/<int:id>/confirmed', methods=['DELETE'])
def cancel_accepted_offer(id):
    confirmed_order = ConfirmedOrder.query.get(id)

    if confirmed_order is None:
        abort(404, f"La oferta confirmada con ID {id} no fue encontrada")

    # Elimina la entrada de la tabla de órdenes confirmadas
    db.session.delete(confirmed_order)
    db.session.commit()

    return {'message': f'Oferta confirmada con ID {id} cancelada correctamente'}, 200
from flask import Blueprint, request, jsonify
from . import api_bp
from .errors import not_found, bad_request
from ..models import Order, Product
from .helper_json import json_request, json_response
from flask import current_app, request

@api_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    # Ejemplo: Crear una nueva oferta en la base de datos
    order = Order(product_id=data.get('product_id'), buyer_id=data.get('buyer_id'), offer=data.get('offer'))
    order.save()
    return jsonify({"data": order.to_dict(), "success": True}), 201
    
   
# Editar una orden
@api_bp.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get(id)
    if order:
        data = request.json
        order.offer = data.get('offer')
        if order.save():  # Guardar el pedido y confirmar la transacción
            return jsonify({"data": order.to_dict(), "success": True}), 200
        else:
            return jsonify({"error": "Internal Server Error", "message": "Error updating order", "success": False}), 500
    else:
        return jsonify({"error": "Not Found", "message": "Order not found", "success": False}), 404

    



# Eliminar una orden
@api_bp.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    if order:
        order.delete()
        return jsonify({"success": True}), 200
    else:
        return jsonify({"error": "Not Found", "message": "Order not found", "success": False}), 404
