#!/usr/bin/python3
"""
cities view module for CRUD operations
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    cities with a given state id
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    cities_list = []
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """
    get city object with given id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """
    delete city object with given id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def add_city(state_id):
    """
    add new city object to the given state
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    req = request.get_json(force=True)
    if not isinstance(req, dict):
        abort(400, "Not a JSON")
    if 'name' not in req:
        abort(400, "Missing name")
    req['state_id'] = state_id
    new_city = City(**req)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """
    update city object with given id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    req = request.get_json(force=True)
    if not isinstance(req, dict):
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
