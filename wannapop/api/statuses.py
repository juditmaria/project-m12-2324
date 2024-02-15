from flask import Blueprint, request, jsonify
from . import api_bp
from ..models import Status
from .errors import not_found, bad_request
from .helper_json import json_request, json_response
from flask import current_app, request

@api_bp.route('/statuses', methods=['GET'])
def list_statuses():
    statuses = Status.query.all()
    data = [status.to_dict() for status in statuses]
    return jsonify({"data": data, "success": True})