#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():

    response = make_response(
        [game.to_dict() for game in  Game.query.all()],
        200
    )

    return response

@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    
    game_dict = game.to_dict()

    response = make_response(
        game_dict,
        200
    )

    return response

@app.route('/reviews/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def review_by_id(id):
    review = Review.query.filter(Review.id==id).first_or_404()
    
    if request.method == 'GET':
        response = make_response(review.to_dict(), 200, {'Content-Type': 'application/json'})
    elif request.method == 'PATCH':
        import ipdb; ipdb.set_trace()
        for attr in request.json:
            setattr(review, attr, request.json.get(attr))
        db.session.add(review)
        db.session.commit()
        response = make_response(review.to_dict(), 200)

    elif request.method == 'DELETE':
        db.session.delete(review)
        db.session.commit()
        
        response = make_response({}, 204)

    return response

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'GET':
        reviews = []
        for review in Review.query.all():
            review_dict = review.to_dict()
            reviews.append(review_dict)

        response = make_response(
            reviews,
            200
        )
    elif request.method == 'POST':
        new_review = Review(
            score=request.json.get("score"),
            comment=request.json.get("comment"),
            game_id=request.json.get("game_id"),
            user_id=request.json.get("user_id"),
        )
        
        db.session.add(new_review)
        db.session.commit()
        
        response = make_response(
            new_review.to_dict(),
            201
        )
        

    return response

@app.route('/users')
def users():

    users = []
    for user in User.query.all():
        user_dict = user.to_dict()
        users.append(user_dict)

    response = make_response(
        users,
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
