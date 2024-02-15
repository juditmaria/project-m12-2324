from . import api_bp
from .errors import not_found, bad_request
from ..models import Item, Store, Discount
from .helper_json import json_request, json_response
from flask import current_app, request

# List
@api_bp.route('/items', methods=['GET'])
def get_items():
    search = request.args.get('search')
    if search:
        # Watch SQL at terminal
        Item.db_enable_debug()
        # Filter using query param
        my_filter = Item.nom.like('%' + search + '%')
        items_with_store = Item.db_query_with(Store).filter(my_filter)
    else:
        # No filter
        items_with_store = Item.get_all_with(Store)
    data = Item.to_dict_collection(items_with_store)
    return json_response(data)

# Create
@api_bp.route('/items', methods=['POST'])
def create_item():
    try:
        data = json_request(['nom', 'store_id', 'unitats'])
    except Exception as e:
        current_app.logger.debug(e)
        return bad_request(str(e))
    else:
        item = Item.create(**data)
        current_app.logger.debug("CREATED item: {}".format(item.to_dict()))
        return json_response(item.to_dict(), 201)

# Read
@api_bp.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    result = Item.get_with(id, Store, Discount)
    if result:
        (item, store, discount) = result
        # Serialize data
        data = item.to_dict()
        # Add relationships
        data["store"] = store.to_dict()
        del data["store_id"]
        if (discount):
            data["discount"] = discount.discount
        return json_response(data)
    else:
        current_app.logger.debug("Item {} not found".format(id))
        return not_found("Item not found")

# Update
@api_bp.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.get(id)
    if item:
        try:
            data = json_request(['nom', 'store_id', 'unitats'], False)
        except Exception as e:
            current_app.logger.debug(e)
            return bad_request(str(e))
        else:
            item.update(**data)
            current_app.logger.debug("UPDATED item: {}".format(item.to_dict()))
            return json_response(item.to_dict())
    else:
        current_app.logger.debug("Item {} not found".format(id))
        return not_found("Item not found")

# Delete
@api_bp.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.get(id)
    if item:
        item.delete()
        current_app.logger.debug("DELETED item: {}".format(id))
        return json_response(item.to_dict())
    else:
        current_app.logger.debug("Item {} not found".format(id))
        return not_found("Item not found")