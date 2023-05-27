#!/usr/bin/python3
'''states module'''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
@app_views.route('/states/<state_id>', strict_slashes=False)
def get_states(state_id=None):
    '''Retrieves a state'''
    if state_id is None:
        return jsonify([s.to_dict() for s in storage.all(State).values()])
    else:
        s = storage.get(State, state_id)
        if s:
            return jsonify(s.to_dict())
        else:
            abort(404)


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id=None):
    '''Deletes a state from the storage'''
    s = storage.get(State, state_id)
    if s is None:
        abort(404)
    storage.delete(s)
    storage.save()
    return {}, 200


@app_views.route('/states', strict_slashes=False,
                 methods=['POST'])
def add_state():
    '''Adding a new state in the storage'''
    kwargs = request.get_json()
    if not kwargs or type(kwargs) is not dict:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in kwargs:
        return jsonify({'error': 'Missing name'}), 400
    s = State(**kwargs)
    s.name = str(kwargs.get('name', None))
    storage.new(s)
    storage.save()
    return jsonify(s.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['PUT'])
def update_state(state_id=None):
    '''Update a state'''
    if not state_id or not storage.get(State, state_id):
        abort(404)

    kwargs = request.get_json()
    if not kwargs:
        return jsonify({'error': 'Not a JSON'}), 400
    avoid_them = ['id', 'created_at', 'updated_at']
    s = storage.get(State, state_id)
    for k, v in kwargs.items():
        if k not in avoid_them:
            setattr(s, k, v)
    storage.new(s)
    storage.save()
    return jsonify(s.to_dict()), 200
