from flask import abort
from . import api_bp
from ..models import Order, ConfirmedOrder, db

@api_bp.route('/orders/<int:id>/confirmed', methods=['POST'])
def accept_offer(id):
    order = Order.query.get(id)

    if order is None:
        abort(404, f"La oferta con ID {id} no fue encontrada")

    # Crea una entrada en la tabla de órdenes confirmadas
    confirmed_order = ConfirmedOrder(order_id=id)
    db.session.add(confirmed_order)
    db.session.commit()

    return {'message': f'Oferta con ID {id} aceptada correctamente'}, 200

@api_bp.route('/orders/<int:id>/confirmed', methods=['DELETE'])
def cancel_accepted_offer(id):
    confirmed_order = ConfirmedOrder.query.get(id)

    if confirmed_order is None:
        abort(404, f"La oferta confirmada con ID {id} no fue encontrada")

    # Elimina la entrada de la tabla de órdenes confirmadas
    db.session.delete(confirmed_order)
    db.session.commit()

    return {'message': f'Oferta confirmada con ID {id} cancelada correctamente'}, 200
