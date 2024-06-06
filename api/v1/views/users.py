#!/usr/bin/python3
"""
view for User object that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users/', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects
    """
    users = storage.all(User)
    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieves a user object with the given id
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    delete a user object with given id
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'],
                 strict_slashes=False)
def add_user():
    """
    add new user object
    """
    req = request.get_json(force=True)
    if not isinstance(req, dict):
        abort(400, "Not a JSON")
    if 'email' not in req:
        abort(400, "Missing email")
    if 'password' not in req:
        abort(400, "Missing password")
    new_user = User(**request.json)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    update user object with given id
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    req = request.get_json(force=True)
    if not isinstance(req, dict):
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
