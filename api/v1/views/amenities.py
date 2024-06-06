#!/usr/bin/python3
"""
view for Amenity objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects
    """
    amenities = storage.all(Amenity)
    amenities_list = []
    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """
    Retrieves an amenity object with the given id
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    delete an amenity object with given id
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
def add_amenity():
    """
    add new amenity object
    """
    req = request.get_json(force=True)
    if not isinstance(req, dict):
        abort(400, "Not a JSON")
    if 'name' not in req:
        abort(400, "Missing name")
    new_amenity = Amenity(**request.json)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """
    update an amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    req = request.get_json(force=True)
    if not isinstance(req, dict):
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
