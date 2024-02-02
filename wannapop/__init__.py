from flask import Flask, current_app
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_principal import Principal
from werkzeug.local import LocalProxy
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate  # Agrega esta línea
from .helper_mail import MailManager

# https://stackoverflow.com/a/31764294
logger = LocalProxy(lambda: current_app.logger)

db_manager = SQLAlchemy()
login_manager = LoginManager()
principal_manager = Principal()
mail_manager = MailManager()
toolbar = DebugToolbarExtension()
migrate = Migrate()  # Crea una instancia de Flask-Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    login_manager.init_app(app)
    db_manager.init_app(app)
    principal_manager.init_app(app)
    mail_manager.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db_manager)  # Inicializa Flask-Migrate con tu aplicación y SQLAlchemy

    with app.app_context():
        from . import commands, routes_main, routes_auth, routes_admin, routes_products, routes_category, routes_status

        app.register_blueprint(routes_main.main_bp)
        app.register_blueprint(routes_auth.auth_bp)
        app.register_blueprint(routes_admin.admin_bp)
        app.register_blueprint(routes_products.products_bp)
        app.register_blueprint(routes_category.category_bp)
        app.register_blueprint(routes_status.status_bp)

        app.cli.add_command(commands.db_cli)

    app.logger.info("Aplicació iniciada")

    return app
