#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, abort
from flask_migrate import Migrate
from models import db, Bakery, BakedGood
from sqlalchemy.orm import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakery_list = [bakery.to_dict() for bakery in bakeries]
    return make_response(jsonify(bakery_list), 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    session: Session = db.session
    bakery = session.get(Bakery, id)
    if not bakery:
        abort(404)
    return make_response(jsonify(bakery.to_dict()), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    goods_list = [bg.to_dict() for bg in baked_goods]
    return make_response(jsonify(goods_list), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if not most_expensive:
        abort(404)
    return make_response(jsonify(most_expensive.to_dict()), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
