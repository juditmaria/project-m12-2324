from . import api_bp
from datetime import datetime, timedelta, timezone
from flask import request, abort
from .helper_auth import basic_auth, token_auth
from .helper_json import json_response
from ..models import User, db
import secrets
import logging

@api_bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return json_response({'token': token})

@api_bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token = request.headers.get('Authorization').split()[1]
    user = User.check_token(token)
    if user:
        user.revoke_token()
        return '', 204
    else:
        logging.error("Unauthorized access attempt")
        abort(401)
