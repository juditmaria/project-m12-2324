from . import api_bp
from .errors import not_found
from ..models import Store, Item
from .helper_json import json_response
from flask import current_app

# List
@api_bp.route('/stores', methods=['GET'])
def get_stores():
    stores = Store.get_all()
    data = Store.to_dict_collection(stores)
    return json_response(data)

# Read
@api_bp.route('/stores/<int:id>', methods=['GET'])
def get_store(id):
    store = Store.get(id)
    if store:
        data = store.to_dict()
        return json_response(data)
    else:
        current_app.logger.debug("Store {} not found".format(id))
        return not_found("Store not found")

# Items list
@api_bp.route('/stores/<int:id>/items', methods=['GET'])
def get_store_items(id):
    items = Item.get_all_filtered_by(store_id=id)
    data = Item.to_dict_collection(items)
    return json_response(data)