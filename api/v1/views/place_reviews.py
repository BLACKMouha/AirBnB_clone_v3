#!/usr/bin/python3
'''reviews module'''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from models.city import City


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_place_reviews(place_id=None):
    '''Retrieves all reviews of a place'''
    p = storage.get(Place, place_id)
    if p:
        return jsonify([r.to_dict() for r in p.reviews])
    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id=None):
    '''Retrieves a review'''
    r = storage.get(Review, review_id)
    if r:
        return jsonify(r.to_dict()), 200
    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id=None):
    '''Deletes a review from the storage'''
    r = storage.get(Review, review_id)
    if r is None:
        abort(404)
    storage.delete(r)
    storage.save()
    return {}, 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def add_review(place_id=None):
    '''Adding a new review in the storage'''
    p = storage.get(Place, place_id)
    if not p:
        abort(404)
    kwargs = request.get_json()
    if not kwargs or type(kwargs) is not dict:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in kwargs:
        return jsonify({'error': 'Missing user_id'}), 400
    u = storage.get(User, kwargs.get('user_id', None))
    if not u:
        abort(404)
    if 'text' not in kwargs:
        return jsonify({'error': 'Missing text'}), 400
    r = Review(**kwargs)
    r.place_id = place_id
    storage.new(r)
    storage.new(p)
    storage.save()
    return jsonify(r.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id=None):
    '''Update a review'''
    if not storage.get(Review, review_id):
        abort(404)
    kwargs = request.get_json()
    if not kwargs:
        return jsonify({'error': 'Not a JSON'}), 400
    avoid_them = ['id', 'created_at', 'updated_at']
    r = storage.get(Review, review_id)
    for k, v in kwargs.items():
        if k not in avoid_them:
            setattr(r, k, v)
    storage.new(r)
    storage.save()
    return jsonify(r.to_dict()), 200
