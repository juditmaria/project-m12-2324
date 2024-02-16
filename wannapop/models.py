from flask_login import UserMixin
from . import db_manager as db
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash
from .mixins import BaseMixin, SerializableMixin
from datetime import timedelta, timezone, datetime
import secrets

class User(UserMixin, db.Model, SerializableMixin, BaseMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String, nullable=False)
    __password = db.Column("password", db.String, nullable=False)
    verified = db.Column(db.Integer, nullable=False)
    email_token = db.Column(db.String, nullable=True, server_default=None)
    created = db.Column(db.DateTime, server_default=func.now())
    updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    
    token = db.Column(db.String, unique=True, nullable=True)
    token_expiration = db.Column(db.DateTime, nullable=True)

    def get_id(self):
        return self.email
    
    def get_token(self, expires_in=3600):
        now = datetime.now(timezone.utc)
        if self.token and self.token_expiration.replace(tzinfo=timezone.utc) > now + timedelta(seconds=60):
            return self.token
        self.token = secrets.token_hex(16)
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        db.session.commit()
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.now(timezone.utc) - timedelta(seconds=1)
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check_token(token):
        user = User.get_filtered_by(token=token)
        if user is None or user.token_expiration.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return None
        return user
    
    @hybrid_property
    def password(self):
        return ""
    
    @password.setter
    def password(self, plain_text_password):
        self.__password = generate_password_hash(plain_text_password, method="scrypt")

    def check_password(self, some_password):
        return check_password_hash(self.__password, some_password)

    def is_admin(self):
        return self.role == "admin"

    def is_moderator(self):
        return self.role == "moderator"
    
    def is_admin_or_moderator(self):
        return self.is_admin() or self.is_moderator()
    
    def is_wanner(self):
        return self.role == "wanner"

    def is_action_allowed_to_product(self, action, product=None, banned=None):
        from .helper_role import _permissions, Action

        current_permissions = _permissions[self.role]
        if not current_permissions:
            return False
        
        if not action in current_permissions:
            return False
        
        if action == Action.products_update and self.is_wanner():
            return product and self.id == product.seller_id
        
        if action == Action.products_delete and self.is_wanner():
            return product and self.id == product.seller_id
        
        if action == Action.products_read and self.is_wanner():
            return product and (not banned or self.id == product.seller_id)
        
        return True

class Product(db.Model, SerializableMixin, BaseMixin):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    photo = db.Column(db.String, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey("statuses.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created = db.Column(db.DateTime, server_default=func.now())
    updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Category(db.Model, SerializableMixin, BaseMixin):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False)

class Status(db.Model, SerializableMixin, BaseMixin):
    __tablename__ = "statuses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False)

class BlockedUser(db.Model, SerializableMixin, BaseMixin):
    __tablename__ = "blocked_users"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    message = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, server_default=func.now())

class BannedProduct(db.Model, SerializableMixin, BaseMixin):
    __tablename__ = "banned_products"
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    reason = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, server_default=func.now())


#Taula order
class Order(db.Model, BaseMixin, SerializableMixin):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    offer = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    created = db.Column(db.DateTime, server_default=func.now())

# Taula confirmed_orders
class ConfirmedOrder(db.Model, BaseMixin, SerializableMixin):
    __tablename__ = "confirmed_orders"
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), primary_key=True)
    created = db.Column(db.DateTime, server_default=func.now())
