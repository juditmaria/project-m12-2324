from flask import Blueprint

api_bp = Blueprint('api', __name__)

# necessari per a que es carreguin les rutes
from . import  users, statuses, orders, errors, tokens, helper_auth

