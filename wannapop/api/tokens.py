# tokens.py

from . import api_bp
from datetime import datetime, timedelta, timezone
from flask import request, abort
from .helper_auth import basic_auth, token_auth
from .helper_json import json_response
from ..models import User, db
import secrets
import logging

logger = logging.getLogger(__name__)

@api_bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    try:
        user = basic_auth.current_user()
        token = user.get_token()
        logger.info(f"Token generated for user: {user.email}")
        return json_response({'token': token})
    except Exception as e:
        logger.error(f"Error generating token: {str(e)}")
        abort(500)

@api_bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    try:
        token = request.headers.get('Authorization').split()[1]
        user = User.check_token(token)
        if user:
            user.revoke_token()
            logger.info(f"Token revoked for user: {user.email}")
            return '', 204
        else:
            logger.error("Unauthorized access attempt")
            abort(401)
    except Exception as e:
        logger.error(f"Error revoking token: {str(e)}")
        abort(500)
