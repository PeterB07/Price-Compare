from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tracked_products = db.relationship('Product', secondary='user_product_tracking', back_populates='tracked_by')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    prices = db.relationship('Price', backref='store', lazy='dynamic')

    def __repr__(self):
        return f'<Store {self.name}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    category = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    prices = db.relationship('Price', backref='product', lazy='dynamic')
    tracked_by = db.relationship('User', secondary='user_product_tracking', back_populates='tracked_products')

    def __repr__(self):
        return f'<Product {self.name}>'

    def get_current_prices(self):
        return Price.query.filter_by(product_id=self.id).order_by(Price.created_at.desc()).all()

    def get_lowest_price(self):
        return Price.query.filter_by(product_id=self.id).order_by(Price.price).first()

class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    url = db.Column(db.String(500))  # URL to the product page
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_available = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Price {self.price} for Product {self.product_id} at Store {self.store_id}>'

# Association table for user-product tracking
user_product_tracking = db.Table('user_product_tracking',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow),
    db.Column('notify_price_drop', db.Boolean, default=True),
    db.Column('target_price', db.Float)
)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))