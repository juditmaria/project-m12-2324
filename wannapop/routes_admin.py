from flask import Blueprint, render_template
from .models import User, Product, Category, Status, BannedProduct  
from .helper_role import Role, role_required
from . import db_manager as db
from .helper_role import Action, perm_required
from flask import current_app, request, redirect, url_for
from .forms import BanForm, DeleteForm

# Blueprint
admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route('/admin')
@role_required(Role.admin, Role.moderator)
def admin_index():
    return render_template('admin/index.html')

@admin_bp.route('/admin/users')
@role_required(Role.admin)
def admin_users():
    users = db.session.query(User).all()
    return render_template('admin/users_list.html', users=users)

@admin_bp.route('/products/ban/<int:product_id>', methods=['GET', 'POST'])
@role_required(Role.moderator)
@perm_required(Action.products_read)
def product_ban(product_id):
    result = db.session.query(Product, Category, Status).join(Category).join(Status).filter(Product.id == product_id).one_or_none()
    product = db.session.query(Product).filter(Product.id == product_id).one_or_none()

    (product, category, status) = result

    form = BanForm(request.form)
    if request.method == 'POST' and form.validate():
        banned_product = BannedProduct(product_id=product.id, justification=form.reason.data)
        db.session.add(banned_product)
        db.session.commit()

        return redirect(url_for('admin_bp.admin_index'))

    return render_template('products/ban.html', product=product, category=category, status=status, form=form)


@admin_bp.route('/products/unban/<int:product_id>', methods=['GET', 'POST'])
@role_required(Role.moderator)
@perm_required(Action.products_read)
def product_unban(product_id):
    result = db.session.query(Product, Category, Status).join(Category).join(Status).filter(Product.id == product_id).one_or_none()
    product = db.session.query(Product).filter(Product.id == product_id).one_or_none()

    (product, category, status) = result

    form = DeleteForm(request.form)  

    if request.method == 'POST' and form.validate():
        banned_product = db.session.query(BannedProduct).filter_by(product_id=product.id).first()
        if banned_product:
            db.session.delete(banned_product)
            db.session.commit()

        return redirect(url_for('admin_bp.admin_index'))

    return render_template('products/unban.html', product=product, category=category, status=status, form=form)
