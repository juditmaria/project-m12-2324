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
        flash("User account not blocked", "error")
        return redirect(url_for('admin_bp.admin_users'))

    if user.is_admin_or_moderator():
        flash("Only 'wanner' users can be blocked", "error")
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
    product = Product.query.get(product_id)
    if not product:
        abort(404)
    
    form = BanProductForm()
    if form.validate_on_submit():
        reason = form.reason.data
        return ProductMixin.ban_product(product, reason)
    
    return render_template('admin/products/ban.html', product=product, form=form)

@admin_bp.route('/admin/products/<int:product_id>/unban', methods=["GET", "POST"])
@role_required(Role.moderator)
def unban_product(product_id):
    banned_product = BannedProduct.query.get(product_id)
    if not banned_product:
        abort(404)
    
    return ProductMixin.unban_product(banned_product)
