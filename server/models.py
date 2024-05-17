from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
    }
)

db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

class User(db.Model, SerializerMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email_address = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    allergic_info = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    Eats = db.relationship('Eats', back_populates='User', lazy=True)
    Dibs = db.relationship('Dibs', back_populates='User', lazy=True)
    given_reviews = db.relationship('Review', back_populates='User', foreign_keys='Review.user_id', lazy=True)
    received_reviews = db.relationship('Review', back_populates='User', foreign_keys='Review.eats_id', lazy=True)

    eat_names = association_proxy('Eats', 'eats_name')
    dib_statuses = association_proxy('Dibs', 'dib_status')
    given_review_ratings = association_proxy('given_reviews', 'rating')
    received_review_ratings = association_proxy('received_reviews', 'rating')

    serialize_rules = ('-password',)

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username cannot be empty")
        return username

    @validates('email_address')
    def validate_email(self, key, email):
        if not email or '@' not in email:
            raise ValueError("Invalid email address")
        return email

class Eats(db.Model, SerializerMixin):
    __tablename__ = "eats"

    id = db.Column(db.Integer, primary_key=True)
    eats_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    cook_time = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    allergic_ingredient = db.Column(db.String(300), nullable=True)
    perishable = db.Column(db.Boolean, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    User = db.relationship('User', back_populates='Eats')
    food_tags = db.relationship('FoodTag', secondary='eats_food_tag', lazy='subquery', back_populates='Eats')
    Dibs = db.relationship('Dibs', back_populates='Eats', lazy=True)
    reviews = db.relationship('Review', back_populates='Eats', lazy=True)

    tags = association_proxy('food_tags', 'name')
    dib_statuses = association_proxy('Dibs', 'dib_status')
    review_ratings = association_proxy('reviews', 'rating')

    serialize_rules = ()

    @validates('eats_name')
    def validate_eats_name(self, key, eats_name):
        if not eats_name:
            raise ValueError("Eats name cannot be empty")
        return eats_name

    @validates('quantity')
    def validate_quantity(self, key, quantity):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        return quantity

class Dibs(db.Model, SerializerMixin):
    __tablename__ = "dibs"

    id = db.Column(db.Integer, primary_key=True)
    dib_status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    eats_id = db.Column(db.Integer, db.ForeignKey('eats.id'), nullable=False)

    User = db.relationship('User', back_populates='Dibs')
    Eats = db.relationship('Eats', back_populates='Dibs')

    user_names = association_proxy('User', 'username')
    eats_names = association_proxy('Eats', 'eats_name')

    serialize_rules = ()

    @validates('dib_status')
    def validate_dib_status(self, key, dib_status):
        if not dib_status:
            raise ValueError("Dib status cannot be empty")
        return dib_status

class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    eats_id = db.Column(db.Integer, db.ForeignKey('eats.id'), nullable=False)

    User = db.relationship('User', back_populates='given_reviews')
    Eats = db.relationship('Eats', back_populates='reviews')

    user_names = association_proxy('User', 'username')
    eats_names = association_proxy('Eats', 'eats_name')

    serialize_rules = ()

    @validates('rating')
    def validate_rating(self, key, rating):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating

class FoodTag(db.Model, SerializerMixin):
    __tablename__ = "food_tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    Eats = db.relationship('Eats', secondary='eats_food_tag', lazy='subquery', back_populates='food_tags')

    serialize_rules = ()

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Tag name cannot be empty")
        return name

class EatsFoodTag(db.Model):
    __tablename__ = "eats_food_tag"

    eats_id = db.Column(db.Integer, db.ForeignKey('eats.id'), primary_key=True)
    food_tag_id = db.Column(db.Integer, db.ForeignKey('food_tag.id'), primary_key=True)

if __name__ == '__main__':
    app.run(port=5555, debug=True)