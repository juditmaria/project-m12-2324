from flask import Blueprint, render_template, abort, flash, redirect, url_for
from .models import User, BlockedUser, Product, BannedProduct
from .helper_role import Role, role_required
from .forms import ConfirmForm, BlockUserForm, BanProductForm
from . import db_manager as db
from .models import User, BlockedUser
from .mixins import BaseMixin, SerializableMixin


# Blueprint
admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route('/admin')
@role_required(Role.admin, Role.moderator)
def admin_index():
    return render_template('admin/index.html')

@admin_bp.route('/admin/users')
@role_required(Role.admin)
def admin_users():
    users = db.session.query(User, BlockedUser).outerjoin(BlockedUser).order_by(User.id.asc()).all()
    return render_template('admin/users/list.html', users=users)

@admin_bp.route('/admin/users/<int:user_id>/block', methods=["GET", "POST"])
@role_required(Role.admin)
def block_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    
    if user.is_admin_or_moderator():
        flash("Sols es poden bloquejar els usuaris wanner", "error")
        return redirect(url_for('admin_bp.admin_users'))

    blocked = BlockedUser.query.filter_by(user_id=user.id).first()
    if blocked:
        flash("Compte d'usuari/a ja bloquejat", "error")
        return redirect(url_for('admin_bp.admin_users'))

    form = BlockUserForm()
    if form.validate_on_submit():
        new_block = BlockedUser.create(user_id=user.id, message=form.message.data)
        if new_block:
            flash("Compte d'usuari/a bloquejat", "success")
            return redirect(url_for('admin_bp.admin_users'))
        else:
            flash("Error en bloquejar el compte d'usuari/a", "error")

    return render_template('admin/users/block.html', user=user, form=form)

@admin_bp.route('/admin/users/<int:user_id>/unblock', methods=["GET", "POST"])
@role_required(Role.admin)
def unblock_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)

    blocked = BlockedUser.query.filter_by(user_id=user.id).first()
    if not blocked:
        flash("Compte d'usuari/a no bloquejat", "error")
        return redirect(url_for('admin_bp.admin_users'))

    if user.is_admin_or_moderator():
        flash("Sols es poden bloquejar els usuaris wanner", "error")
        return redirect(url_for('admin_bp.admin_users'))
    
    form = ConfirmForm()
    if form.validate_on_submit():
        if blocked.delete():
            flash("Compte d'usuari/a desbloquejat", "success")
            return redirect(url_for('admin_bp.admin_users'))
        else:
            flash("Error en desbloquejar el compte d'usuari/a", "error")

    return render_template('admin/users/unblock.html', user=user, form=form)

@admin_bp.route('/admin/products/<int:product_id>/ban', methods=["GET", "POST"])
@role_required(Role.moderator)
def ban_product(product_id):
    result = db.session.query(Product, BannedProduct).outerjoin(BannedProduct).filter(Product.id == product_id).one_or_none()
    if not result:
        abort(404)
    
    (product, banned) = result

    if banned:
        flash("Producte ja prohibit", "error")
        return redirect(url_for('products_bp.product_list'))

    form = BanProductForm()
    if form.validate_on_submit():
        new_banned = BannedProduct();
        # carregar dades de la URL
        new_banned.product_id = product.id
        # carregar dades del formulari
        form.populate_obj(new_banned)
        # insert!
        db.session.add(new_banned)
        db.session.commit()
        # retornar al llistat
        flash("Producte prohibit", "success")
        return redirect(url_for('products_bp.product_list'))

    return render_template('admin/products/ban.html', product=product, form=form)

@admin_bp.route('/admin/products/<int:product_id>/unban', methods=["GET", "POST"])
@role_required(Role.moderator)
def unban_product(product_id):
    result = db.session.query(Product, BannedProduct).outerjoin(BannedProduct).filter(Product.id == product_id).one_or_none()
    if not result:
        abort(404)
    
    (product, banned) = result
    
    if not banned:
        flash("Producte no prohibit", "error")
        return redirect(url_for('products_bp.product_list'))
    
    form = ConfirmForm()
    if form.validate_on_submit():
        db.session.delete(banned)
        db.session.commit()
        flash("Producte permès", "success")
        return redirect(url_for('products_bp.product_list'))

    return render_template('admin/products/unban.html', product=product, form=form)
