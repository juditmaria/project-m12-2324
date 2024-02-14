from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user, login_required, login_user, logout_user
from . import db_manager as db
from . import db_manager as db, login_manager, mail_manager, logger
from .models import User, BlockedUser
from .mixins import BaseMixin, SerializableMixin
from .forms import LoginForm, RegisterForm, ResendForm
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from .helper_role import notify_identity_changed, Role
import secrets
from markupsafe import Markup

# Blueprint
auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = db.session.query(User).filter(User.email == email).one_or_none()
        if user and user.check_password(password):
            if not user.verified:
                flash("Revisa el teu email i verifica el teu compte", "error")
                return redirect(url_for("auth_bp.login"))
            
            login_user(user)
            notify_identity_changed()

            return redirect(url_for("main_bp.init"))

        flash("Error d'usuari i/o contrasenya", "error")
        return redirect(url_for("auth_bp.login"))
    
    return render_template('auth/login.html', form=form)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Si ya está autenticado, salimos de aquí
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))

    form = RegisterForm()
    if form.validate_on_submit(): # si se ha enviado el formulario via POST y es correcto
        new_user = User()
       
        # datos del formulario al objeto new_user
        form.populate_obj(new_user)

        # los nuevos usuarios tienen rol 'wanner'
        new_user.role = Role.wanner

        # los nuevos usuarios deben verificar el email
        new_user.verified = False
        new_user.email_token = secrets.token_urlsafe(20)

        # insert!
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            logger.error(f"No se ha insertado el usuario/a {new_user.email} en BD")
            flash("Nombre de usuario/a y/o correo electrónico duplicado", "danger")
        else:
            logger.info(f"Usuario {new_user.email} se ha registrado correctamente")
            # envío el email!
            try:
                mail_manager.send_register_email(new_user.name, new_user.email, new_user.email_token)
                flash("Revisa tu correo para verificarlo", "success")
            except:
                logger.warning(f"No se ha enviado correo de verificación al usuario/a {new_user.email}")
                flash(Markup("No hemos podido enviar el correo de verificación. Inténtalo más tarde <a href='/resend'>aquí</a>"), "danger")

            return redirect(url_for("auth_bp.login"))
    
    return render_template('auth/register.html', form = form)

@auth_bp.route("/verify/<name>/<token>")
def verify(name, token):
    user = db.session.query(User).filter(User.name == name).one_or_none()
    if user and user.email_token == token:
        user.verified = True
        user.email_token = None
        db.session.commit()
        flash("Compte verificat correctament", "success")
    else:
        flash("Error de verificació", "error")
    return redirect(url_for("auth_bp.login"))

@auth_bp.route("/resend", methods=["GET", "POST"])
def resend():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))

    form = ResendForm()
    if form.validate_on_submit():
        email = form.email.data
        user = db.session.query(User).filter(User.email == email).one_or_none()
        if user:
            if user.verified:
                flash("Aquest compte ja està verificat", "error")
            else:
                # Envío de correo electrónico
                flash("Revisa el teu correu per verificar-lo", "success")
        else:
            flash("Aquest compte no existeix", "error")
        return redirect(url_for("auth_bp.login"))
    else:
        return render_template('auth/resend.html', form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("T'has desconnectat correctament", "success")
    return redirect(url_for("auth_bp.login"))

@login_manager.user_loader
def load_user(email):
    if email is not None:
        return db.session.query(User).filter(User.email == email).one_or_none()
    return None

@login_manager.unauthorized_handler
def unauthorized():
    flash("Autentica't o registra't per accedir a aquesta pàgina", "error")
    return redirect(url_for("auth_bp.login"))
