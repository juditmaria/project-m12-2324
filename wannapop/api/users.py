from flask import Blueprint, request, jsonify
from . import api_bp
from .errors import not_found, bad_request
from ..models import User, Product
from .helper_json import json_request, json_response
from flask import current_app, request

@api_bp.route('/users', methods=['GET'])
def list_users():
    name = request.args.get('name')
    if name:
        users = User.query.filter_by(name=name).all()
    else:
        users = User.query.all()
    data = [user.to_dict() for user in users]
    return jsonify({"data": data, "success": True})

@api_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        data = user.to_dict()
        return jsonify({"data": data, "success": True})
    else:
        return jsonify({"error": "Not Found", "message": "User not found", "success": False}), 404

@api_bp.route('/users/<int:id>/products', methods=['GET'])
def list_user_products(id):
    user = User.query.get(id)
    if user:
        products = Product.query.filter_by(seller_id=id).all()
        data = [product.to_dict() for product in products]
        return jsonify({"data": data, "success": True})
    else:
        return jsonify({"error": "Not Found", "message": "User not found", "success": False}), 404


