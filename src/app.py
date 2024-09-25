"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/', methods=['POST'])
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def handle_getting_people():
#get ALL people
    people = Person.query.all()
    person_dictionaries = []
    for person in people:
        person_dictionaries.append(
            person.serialize()
        )
    return jsonify(person_dictionaries), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_getting_a_person(person_id):
#get a single person
    person_info = Person.query.get({"id": person_id})
    return jsonify(person_info.serialize()), 200


@app.route('/planets', methods=['GET'])
def handle_getting_planets():
#get ALL planets
    planets = Planet.query.all()
    planet_dictionaries = []
    for planet in planets:
        planet_dictionaries.append(
            planet.serialize()
        )
    return jsonify(planet_dictionaries), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_getting_a_planet(planet_id):
#get a single planet
    planet_info = Planet.query.get({"id": planet_id})
    return jsonify(planet_info.serialize()), 200

@app.route('/users', methods=['GET'])
def handle_getting_users():
#get ALL users
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def handle_getting_current_favorites(user_id):
#get ALL favorites of user
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST', 'DELETE'])
def handle_favorite_planet(planet_id):
#add planet to current user's favorites
    if request.method == "POST":
        user_id = request.json.get('user_id')
        favorite = Favorite(user_id=user_id, planet_id=planet_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify(favorite.serialize()), 201
    else:
        user_id = request.json.get('user_id')
        favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": "Favorite planet deleted"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST', 'DELETE'])
def handle_favorite_people(people_id):
#add planet to current user's favorites
    if request.method == "POST":
        user_id = request.json.get('user_id')
        favorite = Favorite(user_id=user_id, character_id=people_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify(favorite.serialize()), 201
    else:
        user_id = request.json.get('user_id')
        favorite = Favorite.query.filter_by(user_id=user_id, character_id=people_id).first()
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": "Favorite person deleted"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
