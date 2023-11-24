from flask import Blueprint, redirect, render_template, url_for, current_app
from flask_login import current_user, login_user, login_required, logout_user
from . import login_manager
from .models import User
from .forms import LoginForm, RegisterForm
from . import db_manager as db
from werkzeug.security import check_password_hash
from flask import request, flash
from werkzeug.security import generate_password_hash

# Blueprint
auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    # Si ja està autenticat, sortim d'aquí
    if current_user.is_authenticated:
        current_app.logger.debug("[login] user is authenticated")
        return redirect(url_for("main_bp.init"))

    form = LoginForm()
    if form.validate_on_submit(): # si s'ha enviat el formulari via POST i és correcte
        email = form.email.data
        plain_text_password = form.password.data
        current_app.logger.debug("[login] loading user")
        user = load_user(email)
        if user and check_password_hash(user.password, plain_text_password):
            # aquí és crea la cookie
            current_app.logger.debug("[login] login OK")
            login_user(user)
            return redirect(url_for("main_bp.init"))

        # si arriba aquí, és que no s'ha autenticat correctament
        current_app.logger.debug("[login] login ERROR")
        return redirect(url_for("auth_bp.login"))
    
    current_app.logger.debug("[login] login form page")
    return render_template('login.html', form = form)

@login_manager.user_loader
def load_user(email):
    if email is not None:
        # select amb 1 resultat o cap
        user_or_none = db.session.query(User).filter(User.email == email).one_or_none()
        return user_or_none
    return None

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth_bp.login"))

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))



@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")
        current_app.logger.debug(password)
        current_app.logger.debug(confirm_password)

        # Verifica si el usuario ya existe
        existing_user = db.session.query(User).filter_by(email=email).first()
        if existing_user:
            flash("El correo electrónico ya está registrado. Inicia sesión en lugar de registrarte.", "danger")
            return redirect(url_for("auth_bp.login"))



        # Crea un nuevo usuario
        new_user = User(email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        flash("Registro exitoso. Inicia sesión con tu nueva cuenta.", "success")
        return redirect(url_for("auth_bp.login"))

    return render_template('register.html', form=form)
