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
from models import db, User, People, Planets, People_Favorite, Planets_Favorite

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
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    user_query = User.query.all()
    user_list = []
    
  
    for user in user_query:
        user_data = user.serialize()
        user_data["favorite_planets"] = list(map(lambda fav: fav.serialize(), user.favorites_planets))
        user_data["favorite_people"] = list(map(lambda fav: fav.serialize(), user.favorites_people))
        user_list.append(user_data)
    
    return jsonify(user_list), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    one_user = User.query.get(user_id)
    if one_user is None:
        return jsonify({"info": "Not found"}), 404

    user_data = one_user.serialize()
    user_data["favorite_planets"] = list(map(lambda fav: fav.serialize(), one_user.favorites_planets))
    user_data["favorite_people"] = list(map(lambda fav: fav.serialize(), one_user.favorites_people))
    
    return jsonify(user_data), 200

@app.route('/people/', methods=['GET'])
def get_people():
    people_query = People.query.all()
    people_list = list(map(lambda people: people.serialize(), people_query))
    return jsonify(people_list), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    one_people = People.query.get(people_id)
    if one_people is None:
        return jsonify({"info": "Not found"}), 404
    return jsonify(one_people.serialize()), 200

@app.route('/planets/', methods=['GET'])
def get_planets():
    planets_query = Planets.query.all()
    planets_list = list(map(lambda planet: planet.serialize(), planets_query))
    return jsonify(planets_list), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_one_planet(planets_id):
    one_planet = Planets.query.get(planets_id)
    if one_planet is None:
        return jsonify({"info": "Not found"}), 404
    return jsonify(one_planet.serialize()), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite_planet = Planets_Favorite.query.filter_by(planet_id=planet_id).first()
    if favorite_planet is None:
        return jsonify({"info": "Not found"}), 404

    db.session.delete(favorite_planet)
    db.session.commit()
    return jsonify({"info": "Favorite planet deleted"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    favorite_people = People_Favorite.query.filter_by(people_id=people_id).first()
    if favorite_people is None:
        return jsonify({"info": "Not found"}), 404

    db.session.delete(favorite_people)
    db.session.commit()
    return jsonify({"info": "Favorite people deleted"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
