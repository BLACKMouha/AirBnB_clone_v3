#!/usr/bin/python3
'''cities module'''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_state_cities(state_id=None):
    '''Retrieves all cities of a state'''
    s = storage.get(State, state_id)
    if s:
        return jsonify([c.to_dict() for c in s.cities])
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id=None):
    '''Retrieves a city'''
    c = storage.get(City, city_id)
    if c:
        return jsonify(c.to_dict()), 200
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id=None):
    '''Deletes a city from the storage'''
    c = storage.get(City, city_id)
    if c is None:
        abort(404)
    storage.delete(c)
    storage.save()
    return {}, 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def add_city(state_id):
    '''Adding a new city in the storage'''
    s = storage.get(State, state_id)
    if not s:
        abort(404)
    kwargs = request.get_json()
    if not kwargs or type(kwargs) is not dict:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in kwargs:
        return jsonify({'error': 'Missing name'}), 400
    c = City(kwargs)
    c.name = str(kwargs.get('name', None))
    c.state_id = state_id
    storage.new(c)
    storage.new(s)
    storage.save()
    return jsonify(c.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def update_city(city_id=None):
    '''Update a city'''
    if not storage.get(City, city_id):
        abort(404)
    kwargs = request.get_json()
    if not kwargs:
        return jsonify({'error': 'Not a JSON'}), 400
    avoid_them = ['id', 'created_at', 'updated_at']
    c = storage.get(City, city_id)
    for k, v in kwargs.items():
        if k not in avoid_them:
            setattr(c, k, v)
    storage.new(c)
    storage.save()
    return jsonify(c.to_dict()), 200
