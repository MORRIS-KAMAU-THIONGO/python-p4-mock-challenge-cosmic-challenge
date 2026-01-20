#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)


@app.route('/')
def home():
    return ''


# Scientists Routes
@app.route('/scientists', methods=['GET'])
def get_scientists():
    scientists = Scientist.query.all()
    return make_response(jsonify([{
        'id': s.id,
        'name': s.name,
        'field_of_study': s.field_of_study
    } for s in scientists]), 200)


@app.route('/scientists/<int:id>', methods=['GET'])
def get_scientist(id):
    scientist = Scientist.query.get(id)
    if scientist:
        return make_response(jsonify(scientist.to_dict()), 200)
    return make_response(jsonify({'error': 'Scientist not found'}), 404)


@app.route('/scientists', methods=['POST'])
def create_scientist():
    try:
        data = request.get_json()
        scientist = Scientist(
            name=data.get('name'),
            field_of_study=data.get('field_of_study')
        )
        db.session.add(scientist)
        db.session.commit()
        return make_response(jsonify(scientist.to_dict()), 201)
    except ValueError as e:
        return make_response(jsonify({'errors': ['validation errors']}), 400)
    except Exception as e:
        return make_response(jsonify({'errors': ['validation errors']}), 400)


@app.route('/scientists/<int:id>', methods=['PATCH'])
def update_scientist(id):
    scientist = Scientist.query.get(id)
    if not scientist:
        return make_response(jsonify({'error': 'Scientist not found'}), 404)
    
    try:
        data = request.get_json()
        if 'name' in data:
            scientist.name = data['name']
        if 'field_of_study' in data:
            scientist.field_of_study = data['field_of_study']
        db.session.commit()
        return make_response(jsonify(scientist.to_dict()), 202)
    except ValueError as e:
        return make_response(jsonify({'errors': ['validation errors']}), 400)
    except Exception as e:
        return make_response(jsonify({'errors': ['validation errors']}), 400)


@app.route('/scientists/<int:id>', methods=['DELETE'])
def delete_scientist(id):
    scientist = Scientist.query.get(id)
    if not scientist:
        return make_response(jsonify({'error': 'Scientist not found'}), 404)
    
    db.session.delete(scientist)
    db.session.commit()
    return make_response(jsonify({}), 204)


# Planets Routes
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return make_response(jsonify([p.to_dict() for p in planets]), 200)


# Missions Routes
@app.route('/missions', methods=['POST'])
def create_mission():
    try:
        data = request.get_json()
        mission = Mission(
            name=data.get('name'),
            scientist_id=data.get('scientist_id'),
            planet_id=data.get('planet_id')
        )
        db.session.add(mission)
        db.session.commit()
        return make_response(jsonify(mission.to_dict()), 201)
    except ValueError as e:
        return make_response(jsonify({'errors': ['validation errors']}), 400)
    except Exception as e:
        return make_response(jsonify({'errors': ['validation errors']}), 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
