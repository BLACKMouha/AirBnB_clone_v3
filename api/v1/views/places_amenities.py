#!/usr/bin/python3
'''places_amenities module'''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_place_amenities(place_id=None):
    '''Retrieves all amenities of a place'''
    p = storage.get(Place, place_id)
    if p:
        if storage_t == 'db':
            return jsonify([a.to_dict() for a in p.amenities])
        else:
            return jsonify([storage.get(Amenity, amenity_id)
                            for amenity_id in p.amenity_ids])
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_place_amenity(place_id=None, amenity_id=None):
    '''Deletes an amenity of a place'''
    p = storage.get(Place, place_id)
    if p is None:
        abort(404)
    a = storage.get(Amenity, amenity_id)
    if a is None:
        abort(404)
    if storage_t == 'db':
        if a not in p.amenities:
            abort(404)
        p.amenities = [i for i in p.amenities if i != a]
    else:
        if a.id not in p.amenity_ids:
            abort(404)
        p.amenity_ids.remove(a.id)
    storage.save()
    return {}, 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['POST'])
def add_place_amenity(place_id=None, amenity_id=None):
    '''Links an amenity to a place in the storage'''
    p = storage.get(Place, place_id)
    if not p:
        abort(404)
    a = storage.get(Amenity, amenit_id)
    if not a:
        abort(404)
    if storage_t == 'db':
        p.amenities.append(a)
    else:
        p.amenity_ids.append(a.id)
    storage.save()
    return jsonify(a.to_dict()), 201
