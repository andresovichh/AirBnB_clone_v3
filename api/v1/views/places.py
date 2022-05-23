#!/usr/bin/python3
""" This is a module that lets us import all our views for places"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State
from models.place import Place

@app_views.route("/cities/<string:city_id>/places", methods=['GET'],
                 strict_slashes=False)

def show_all_places_with_city_id(city_id):
    """ shows all places with given city id """

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    new_list = []
    for place in places:
        new_list.append(place.to_dict())
    return jsonify(new_list)


@app_views.route("/places/<string:place_id>", methods=['GET'],
                 strict_slashes=False)
def show_place_with_id(place_id):
    """ shows place with given id """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<string:place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place_with_id(place_id):
    """ deletes place with given id """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<string:city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place_with_city_id(city_id):
    """ creates place with given city id """

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    place = Place(**data)
    place.city_id = city_id
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/string:place_id", methods=['PUT'],
                 strict_slashes=False)
def update_place_with_id(place_id):
    """ updates place with given id """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' in data:
        place.user_id = data['user_id']
    if 'name' in data:
        place.name = data['name']

    storage.save()
    return jsonify(place.to_dict()), 200