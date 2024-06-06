#!/usr/bin/python3
"""
view for Place objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = city.places
    if not places:
        abort(404)
    places_list = []
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    Retrieves a place object with the given id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    delete a place object with given id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def add_place(city_id):
    """
    add new place object
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    req = request.get_json(force=True)
    if not isinstance(req, dict):
        abort(400, "Not a JSON")
    if 'user_id' not in req:
        abort(400, "Missing user_id")
    if 'name' not in req:
        abort(400, "Missing name")
    user_id = req['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    req['city_id'] = city_id
    new_place = Place(**req)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """
    update place object with given id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    req = request.get_json(force=True)
    if not isinstance(req, dict):
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k not in ['id', 'user_id', 'city_id',
                     'created_at', 'updated_at']:
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200
