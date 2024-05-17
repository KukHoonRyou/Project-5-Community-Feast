#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Local imports
from config import app, db
from models import User, Eats, Dibs, Review, FoodTag

api = Api(app)

# Resource Classes
class UserResource(Resource):
    def get(self, id=None):
        if id:
            user = User.query.get_or_404(id)
            return user.to_dict()
        else:
            users = User.query.all()
            return [user.to_dict() for user in users]

    def post(self):
        data = api.payload
        user = User.from_dict(data)
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

    def patch(self, id):
        user = User.query.get_or_404(id)
        data = api.payload
        user.from_dict(data)
        db.session.commit()
        return user.to_dict()

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class EatsResource(Resource):
    def get(self, id=None):
        if id:
            eat = Eats.query.get_or_404(id)
            return eat.to_dict()
        else:
            eats = Eats.query.all()
            return [eat.to_dict() for eat in eats]

    def post(self):
        data = api.payload
        eat = Eats.from_dict(data)
        db.session.add(eat)
        db.session.commit()
        return eat.to_dict(), 201

    def patch(self, id):
        eat = Eats.query.get_or_404(id)
        data = api.payload
        eat.from_dict(data)
        db.session.commit()
        return eat.to_dict()

    def delete(self, id):
        eat = Eats.query.get_or_404(id)
        db.session.delete(eat)
        db.session.commit()
        return '', 204

class DibsResource(Resource):
    def get(self, id=None):
        if id:
            dib = Dibs.query.get_or_404(id)
            return dib.to_dict()
        else:
            dibs = Dibs.query.all()
            return [dib.to_dict() for dib in dibs]

    def post(self):
        data = api.payload
        dib = Dibs.from_dict(data)
        db.session.add(dib)
        db.session.commit()
        return dib.to_dict(), 201

    def patch(self, id):
        dib = Dibs.query.get_or_404(id)
        data = api.payload
        dib.from_dict(data)
        db.session.commit()
        return dib.to_dict()

    def delete(self, id):
        dib = Dibs.query.get_or_404(id)
        db.session.delete(dib)
        db.session.commit()
        return '', 204

class ReviewResource(Resource):
    def get(self, id=None):
        if id:
            review = Review.query.get_or_404(id)
            return review.to_dict()
        else:
            reviews = Review.query.all()
            return [review.to_dict() for review in reviews]

    def post(self):
        data = api.payload
        review = Review.from_dict(data)
        db.session.add(review)
        db.session.commit()
        return review.to_dict(), 201

    def patch(self, id):
        review = Review.query.get_or_404(id)
        data = api.payload
        review.from_dict(data)
        db.session.commit()
        return review.to_dict()

    def delete(self, id):
        review = Review.query.get_or_404(id)
        db.session.delete(review)
        db.session.commit()
        return '', 204

class FoodTagResource(Resource):
    def get(self, id=None):
        if id:
            foodtag = FoodTag.query.get_or_404(id)
            return foodtag.to_dict()
        else:
            foodtags = FoodTag.query.all()
            return [foodtag.to_dict() for foodtag in foodtags]

    def post(self):
        data = api.payload
        foodtag = FoodTag.from_dict(data)
        db.session.add(foodtag)
        db.session.commit()
        return foodtag.to_dict(), 201

    def patch(self, id):
        foodtag = FoodTag.query.get_or_404(id)
        data = api.payload
        foodtag.from_dict(data)
        db.session.commit()
        return foodtag.to_dict()

    def delete(self, id):
        foodtag = FoodTag.query.get_or_404(id)
        db.session.delete(foodtag)
        db.session.commit()
        return '', 204

# Route Resources
api.add_resource(UserResource, '/users', '/users/<int:id>')
api.add_resource(EatsResource, '/eats', '/eats/<int:id>')
api.add_resource(DibsResource, '/dibs', '/dibs/<int:id>')
api.add_resource(ReviewResource, '/reviews', '/reviews/<int:id>')
api.add_resource(FoodTagResource, '/foodtags', '/foodtags/<int:id>')

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)