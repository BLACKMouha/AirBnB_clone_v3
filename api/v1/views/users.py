#!/usr/bin/python3
'''users module'''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def get_users():
    '''Retrieves all users'''
    return jsonify([u.to_dict() for u in storage.all(User).values()])


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id=None):
    '''Retrieves a user'''
    u = storage.get(User, user_id)
    if u:
        return jsonify(u.to_dict()), 200
    abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id=None):
    '''Deletes a user from the storage'''
    u = storage.get(User, user_id)
    if u is None:
        abort(404)
    storage.delete(u)
    storage.save()
    return {}, 200


@app_views.route('/users', strict_slashes=False,
                 methods=['POST'])
def add_user():
    '''Adding a new user in the storage'''
    kwargs = request.get_json()
    if not kwargs or type(kwargs) is not dict:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in kwargs:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in kwargs:
        return jsonify({'error': 'Missing password'}), 400
    u = User(kwargs)
    u.email = kwargs.get('email', None)
    u.password = kwargs.get('password', None)
    storage.new(u)
    storage.save()
    return jsonify(a.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id=None):
    '''Update a user'''
    if not storage.get(User, user_id):
        abort(404)
    kwargs = request.get_json()
    if not kwargs:
        return jsonify({'error': 'Not a JSON'}), 400
    avoid_them = ['id', 'created_at', 'updated_at', 'email']
    u = storage.get(user, user_id)
    for k, v in kwargs.items():
        if k not in avoid_them:
            setattr(u, k, v)
    storage.new(u)
    storage.save()
    return jsonify(u.to_dict()), 200
