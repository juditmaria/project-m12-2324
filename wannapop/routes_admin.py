from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user
from .models import User, BlockedUser
from .helper_role import Role, role_required
from . import db_manager as db
from flask import current_app

# Blueprint
admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route('/admin')
@role_required(Role.admin, Role.moderator)
def admin_index():
    return render_template('admin/index.html')

@admin_bp.route('/admin/users', methods=['GET', 'POST'])
@role_required(Role.admin)
def admin_users():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        action = request.form.get('action')
        message = request.form.get('message')  # Agregamos la captura del mensaje

        if action and user_id:
            user = User.query.get(user_id)

            if action == 'block':
                block_user(user, message)
            elif action == 'unblock':
                unblock_user(user)

    users = db.session.query(User).all()
    return render_template('admin/users_list.html', users=users)

def block_user(user, message):
    blocked_user = BlockedUser.query.filter_by(user_id=user.id).first()
    if blocked_user:
        flash(f'L\'usuari {user.name} ja està bloquejat.', 'warning')
    else:
        blocked_user = BlockedUser(user_id=user.id, message=message)
        db.session.add(blocked_user)
        db.session.commit()
        flash(f'L\'usuari {user.name} ha estat bloquejat.', 'success')

def unblock_user(user):
    blocked_user = BlockedUser.query.filter_by(user_id=user.id).first()
    if blocked_user:
        db.session.delete(blocked_user)
        db.session.commit()
        flash(f'L\'usuari {user.name} ha estat desbloquejat.', 'success')
    else:
        flash(f'L\'usuari {user.name} no està bloquejat.', 'warning')

@admin_bp.route('/admin/users/<int:user_id>', methods=['GET', 'POST'])
@role_required(Role.admin)
def admin_manage_user(user_id):
    user = User.query.get(user_id)
    if user:
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'block':
                block_user(user, request.form.get('message'))
            elif action == 'unblock':
                unblock_user(user)

        blocked = BlockedUser.query.filter_by(user_id=user.id).first()
        return render_template('admin/manage_user.html', user=user, blocked=blocked)

    flash('Usuari no trobat.', 'error')
    return redirect(url_for('admin_bp.admin_users'))
