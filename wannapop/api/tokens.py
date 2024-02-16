from . import api_bp
from datetime import datetime, timezone
from .helper_auth import basic_auth, token_auth
from .helper_json import json_response
from flask import current_app

@api_bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    current_app.logger.debug("Token:" + token)
    return json_response({'token': token})

@api_bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    return '', 204