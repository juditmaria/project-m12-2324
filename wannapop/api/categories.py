from . import api_bp
from ..models import Category
from .helper_json import json_response

# Listar categorías disponibles
@api_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.get_all()
    # Convertir las categorías en un formato JSONizable
    data = [{"id": category.id, "name": category.name, "slug": category.slug} for category in categories]
    return json_response(data)