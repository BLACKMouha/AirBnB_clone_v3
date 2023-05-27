#!/usr/bin/python3
'''amenities module'''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    '''Retrieves all amenities'''
    return jsonify([a.to_dict() for a in storage.all(Amenity).values()])


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id=None):
    '''Retrieves an amenity'''
    a = storage.get(Amenity, amenity_id)
    if a:
        return jsonify(a.to_dict()), 200
    abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id=None):
    '''Deletes a amenity from the storage'''
    a = storage.get(Amenity, amenity_id)
    if a is None:
        abort(404)
    storage.delete(a)
    storage.save()
    return {}, 200


@app_views.route('/amenities', strict_slashes=False,
                 methods=['POST'])
def add_amenity():
    '''Adding a new amenity in the storage'''
    kwargs = request.get_json()
    if not kwargs or type(kwargs) is not dict:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in kwargs:
        return jsonify({'error': 'Missing name'}), 400
    a = Amenity(kwargs)
    a.name = str(kwargs.get('name', None))
    storage.new(a)
    storage.save()
    return jsonify(a.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id=None):
    '''Update an amenity'''
    if not storage.get(Amenity, amenity_id):
        abort(404)
    kwargs = request.get_json()
    if not kwargs:
        return jsonify({'error': 'Not a JSON'}), 400
    avoid_them = ['id', 'created_at', 'updated_at']
    a = storage.get(Amenity, amenity_id)
    for k, v in kwargs.items():
        if k not in avoid_them:
            setattr(a, k, v)
    storage.new(a)
    storage.save()
    return jsonify(a.to_dict()), 200
