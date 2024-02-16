from ..models import User
from .helper_json import json_error_response
from flask import current_app
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import check_password_hash

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(email, password):
    user = User.get_filtered_by(email=email)
    current_app.logger.debug("credentials: " + email)
    current_app.logger.debug("auth user: " + ("None" if user is None else str(user.to_dict())))
    if user and check_password_hash(user.password, password):
        return user

@basic_auth.error_handler
def basic_auth_error(status):
    return json_error_response(status)

@token_auth.verify_token
def verify_token(token):
    current_app.logger.debug(f"verify_token: {token}")
    return User.check_token(token) if token else None

@token_auth.error_handler
def token_auth_error(status):
    return json_error_response(status)