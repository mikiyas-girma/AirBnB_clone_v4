#!/usr/bin/python3
"""
states view module for CRUD operations
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states/', methods=["GET"])
def get_states():
    """
    Retrieves the list of all State objects
    """
    states = storage.all(State)
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """
    Retrieves a state object with the given id
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404, "Not found")
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    delete a state object with given id
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def add_state():
    """
    add new state object
    """
    req = request.get_json(force=True)
    if not isinstance(req, dict):
        abort(400, "Not a JSON")
    if 'name' not in req:
        abort(400, "Missing name")
    new_state = State(**request.json)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """
    update a state with given id with key value pairs passed
    """
    state_dict = request.get_json(force=True)
    if not isinstance(state_dict, dict):
        abort(400, "Not a JSON")
    state = storage.get(State, state_id)
    if state is None:
        abort(404, "Not found")
    for key, value in state_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
