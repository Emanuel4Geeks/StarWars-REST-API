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
from models import db, User, Personaje, Planeta, Favoritos

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


@app.route("/people", methods=['GET'])
def get_people():
    people_query = Personaje.query.all()
    results = list(map(lambda item: item.serialize(), people_query))

    response_body = {
        "msg": "ok",
        "results": results
    }

    return jsonify(response_body), 200


@app.route("/people/<int:people_id>", methods=['GET'])
def get_people_id(people_id):
    results = Personaje.query.filter_by(id=people_id).first().serialize()

    response_body = {
        "msg": "ok",
        "results": results
    }

    return jsonify(response_body), 200


@app.route("/planets", methods=['GET'])
def get_planets():
    planeta_query = Planeta.query.all()
    results = list(map(lambda item: item.serialize(), planeta_query))

    response_body = {
        "msg": "ok",
        "results": results
    }

    return jsonify(response_body), 200


@app.route("/planets/<int:planet_id>", methods=['GET'])
def get_planet_id(planet_id):
    results = Planeta.query.filter_by(id=planet_id).first().serialize()

    response_body = {
        "msg": "ok",
        "results": results
    }

    return jsonify(response_body), 200


@app.route("/users", methods=['GET'])
def get_users():
    user_query = User.query.all()
    results = list(map(lambda item: item.serialize(), user_query))

    response_body = {
        "msg": "ok",
        "results": results
    }

    return jsonify(response_body), 200


# FAVORITOS
@app.route("/users/favorites", methods=['GET'])
def get_user_favs():
    body = request.json
    results = User.query.filter_by(id=body["id"]).first().favorite_list() or []

    response_body = {
        "msg": "ok",
        "results": results
    }

    return jsonify(response_body), 200

# CREAR FAVORITOS


@app.route("/favorite/planet/<int:planet_id>", methods=['POST'])
def set_fav_planet(planet_id):
    body = request.json

    user_query = User.query.filter_by(id=body["id"]).first()
    planeta_query = Planeta.query.filter_by(id=planet_id).first()

    result = "Imposible asociar el planeta con el usuario de favoritos"
    status = "error"
    code = 400

    if (user_query is not None
            and planeta_query is not None):

        newFav = Favoritos(user_id=body["id"], planeta_id=planet_id)

        db.session.add(newFav)
        db.session.commit()

        result = "Se ha añadido el planeta como favorito"
        status = "ok"
        code = 200

    response_body = {
        "msg": status,
        "results": result
    }

    return jsonify(response_body), code


@app.route("/favorite/people/<int:people_id>", methods=['POST'])
def set_fav_people(people_id):
    body = request.json

    user_query = User.query.filter_by(id=body["id"]).first()
    personaje_query = Personaje.query.filter_by(id=people_id).first()

    result = "Imposible asociar el personajes con el usuario de favoritos"
    status = "error"
    code = 400

    if (user_query is not None
            and personaje_query is not None):
        newFav = Favoritos(user_id=body["id"], personaje_id=people_id)

        db.session.add(newFav)
        db.session.commit()

        result = "Se ha añadido el personaje como favorito"
        status = "ok"
        code = 200

    response_body = {
        "msg": status,
        "results": result
    }

    return jsonify(response_body), code

# BORRAR FAVORITOS


@app.route("/favorite/planet/<int:planet_id>", methods=['DELETE'])
def delete_fav_planet(planet_id):
    body = request.json

    user_query = User.query.filter_by(id=body["id"]).first()
    planeta_query = Planeta.query.filter_by(id=planet_id).first()

    result = "Imposible eliminar el personajes con el usuario de favoritos"
    status = "error"
    code = 400

    if (user_query is not None
            and planeta_query is not None):

        fav_query = Favoritos.query.filter_by(
            user_id=body["id"], planeta_id=planet_id).all()
        if fav_query:
            for fav in fav_query:
                db.session.delete(fav)
            db.session.commit()
            result = "Se han eliminado los planetas como favoritos"
            status = "ok"
            code = 200
        else:
            result = "Imposible eliminar el planeta con el usuario de favoritos"
            status = "error"
            code = 400

    response_body = {
        "msg": status,
        "results": result
    }

    return jsonify(response_body), code


@app.route("/favorite/people/<int:people_id>", methods=['DELETE'])
def delete_fav_people(people_id):
    body = request.json

    user_query = User.query.filter_by(id=body["id"]).first()
    personaje_query = Personaje.query.filter_by(id=people_id).first()

    result = "Imposible eliminar el personajes con el usuario de favoritos"
    status = "error"
    code = 400

    if (user_query is not None
            and personaje_query is not None):

        Favoritos.query.filter_by(
        ).delete()
        fav_query = Favoritos.query.filter_by(
            user_id=body["id"], personaje_id=people_id).all()
        if fav_query:
            for fav in fav_query:
                db.session.delete(fav)
            db.session.commit()
            result = "Se han eliminado los planetas como favoritos"
            status = "ok"
            code = 200
        else:
            result = "Imposible eliminar el planeta con el usuario de favoritos"
            status = "error"
            code = 400

    response_body = {
        "msg": status,
        "results": result
    }

    return jsonify(response_body), code


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
