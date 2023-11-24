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
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    if current_user.is_authenticated:
        # Si el usuario actual ya está autenticado, redirige a la página principal.
        return redirect(url_for("main_bp.init"))

    form = RegisterForm()
    if form.validate_on_submit():
        # Extrae los datos del formulario.
        name = form.name.data
        email = form.email.data
        plain_text_password = form.password.data

        # Comprueba si ya existe un usuario con ese email.
        user = User.query.filter_by(email=email).first()
        if user:
            # Si el usuario ya existe, muestra un mensaje y redirige al formulario de registro.
            flash('Ya existe una cuenta con este correo electrónico.', 'error')
            return redirect(url_for('auth_bp.register'))

        # Si el usuario no existe, crea uno nuevo.
        hashed_password = generate_password_hash(plain_text_password)
        
        new_user = User(
            name=name, 
            email=email, 
            password=hashed_password, 
        )
        current_app.logger.debug(new_user)

        db.session.add(new_user)
        db.session.commit()

        

        # Muestra un mensaje de éxito y redirige a la página de inicio de sesión.
        flash('Registro exitoso. Revisa tu correo electrónico para verificar tu cuenta.', 'success')
        return redirect(url_for('auth_bp.login'))

    # Si el formulario no se ha enviado o no es válido, muestra el formulario de registro.
    return render_template('register.html', form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))
