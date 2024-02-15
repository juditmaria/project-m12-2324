from flask import Blueprint, request, jsonify
from . import api_bp
from .errors import not_found, bad_request
from ..models import Order, Product
from .helper_json import json_request, json_response
from flask import current_app, request

@api_bp.route('/orders', methods=['POST'])
def create_order():
    try:
        data = json_request(['product_id', 'buyer_id', 'offer'])
    except Exception as e:
        current_app.logger.debug(e)
        return bad_request(str(e))
    else:
        order = Order.create(**data)
        current_app.logger.debug("CREATED order: {}".format(order.to_dict()))
        return json_response(order.to_dict(), 201)
    
   
# Editar una orden
@api_bp.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get(id)
    if order:
        try:
            data = json_request(['product_id', 'buyer_id', 'offer'], False)
        except Exception as e:
            current_app.logger.debug(e)
            return bad_request(str(e))
        else:
            order.update(**data)
            current_app.logger.debug("UPDATED order: {}".format(order.to_dict()))
            return json_response(order.to_dict())
    else:
        current_app.logger.debug("Order {} not found".format(id))
        return not_found("Order not found")
    



# Eliminar una orden
@api_bp.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    if order:
        order.delete()
        current_app.logger.debug("DELETED order: {}".format(id))
        return json_response(order.to_dict())
    else:
        current_app.logger.debug("Order {} not found".format(id))
        return not_found("Order not found")