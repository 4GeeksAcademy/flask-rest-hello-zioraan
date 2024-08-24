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
def handle_getting_a_person(id):
#get a single person
    person_info = Person.query.get({"id": id})
    person_dictionary = []
    for person in person_info:
        person_dictionary.append(
            person.serialize()
        )
    
    return jsonify(person_dictionary), 200

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
def handle_getting_a_planet(id):
#get a single planet
    planet_info = Person.query.get({"id": id})
    planet_dictionary = []
    for planet in planet_info:
        planet_dictionary.append(
        planet.serialize()
    )
    return jsonify(planet_dictionary), 200

@app.route('/users', methods=['GET'])
def handle_getting_users():
#get ALL users
    return jsonify(response_body), 200

@app.route('/users/favorites', methods=['GET'])
def handle_getting_current_favorites():
#get ALL favorites of user
    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST', 'DELETE'])
def handle_adding_favorite_planet():
#add planet to current user's favorites
    return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST', 'DELETE'])
def handle_adding_favorite_people():
#add planet to current user's favorites
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
