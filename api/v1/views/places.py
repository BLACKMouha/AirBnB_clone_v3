#!/usr/bin/python3
'''places module'''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_city_places(city_id=None):
    '''Retrieves all places of a city'''
    c = storage.get(City, city_id)
    if c:
        return jsonify([p.to_dict() for p in c.places])
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id=None):
    '''Retrieves a place'''
    p = storage.get(Place, place_id)
    if p:
        return jsonify(p.to_dict()), 200
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id=None):
    '''Deletes a place from the storage'''
    p = storage.get(Place, place_id)
    if p is None:
        abort(404)
    storage.delete(p)
    storage.save()
    return {}, 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def add_place(city_id=None):
    '''Adding a new place in the storage'''
    from models.user import User
    c = storage.get(City, city_id)
    if not c:
        abort(404)
    kwargs = request.get_json()
    if not kwargs or type(kwargs) is not dict:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in kwargs:
        return jsonify({'error': 'Missing user_id'}), 400
    u = storage.get(User, kwargs.get('user_id', None))
    if u is None:
        abort(404)
    if 'name' not in kwargs:
        return jsonify({'error': 'Missing name'}), 400
    p = Place(**kwargs)
    p.city_id = city_id
    storage.new(p)
    storage.new(c)
    storage.save()
    return jsonify(p.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id=None):
    '''Update a place'''
    if not storage.get(Place, place_id):
        abort(404)
    kwargs = request.get_json()
    if not kwargs:
        return jsonify({'error': 'Not a JSON'}), 400
    avoid_them = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
    p = storage.get(Place, place_id)
    for k, v in kwargs.items():
        if k not in avoid_them:
            setattr(p, k, v)
    storage.new(p)
    storage.save()
    return jsonify(p.to_dict()), 200


@app.route('/places_search',
           strict_slashes=False,
           methods=['POST'])
def places_search():
    '''Retrieves all places depending on the JSON body request'''
    rj = request.get_json()
    if type(rj) is not dict:
        return jsonify({'error': 'Not a JSON'}), 400
    if rj:
        return jsonify([p.to_dict() for p in storage.all(Place).values()])
    all_places = []
    if 'states' in rj and rj['states']:
        for s_id in rj['states']:
            s = storage.get(State, s_id)
            for c in s.cities:
                for p in c.places:
                    all_places.append(p)
    if 'cities' in rj and rj['cities']:
        for c_id in rj['cities']:
            c = storage.get(City, c_id)
            for p in c.places:
                all_places.append(p)
    if 'amenities' in rj and rj['amenities']:
        places = storage.all(Places)
        for a_id in rj['amenities']:
            for p in places:
                a = storage.get(Amenity, a_id)
                if a in p.amenities:
                    all_places.append(p)

    return jsonify(all_places)
