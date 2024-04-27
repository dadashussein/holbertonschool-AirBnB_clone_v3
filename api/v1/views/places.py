#!/usr/bin/python3
"""places module"""


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """get all places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    places_list = []
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place():
    request_body = request.get_json(silent=True)
    city_obj = storage.get(City, city_id)

    if city_obj is None:
        abort(404)
    elif not request_body:
        abort(400, "Not a JSON")
    elif "name" not in request_body:
        abort(400, "Missing name")
    elif "user_id" not in request_body:
        abort(400, "Missing user_id")

    user = storage.get(User, request_body["user_id"])
    if user is None:
        abort(404)

    request_body["city_id"] = city_id
    new_place = Place(**request_body)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """get a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """update a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """search for places"""
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    places = storage.all(Place).values()
    places_list = []
    for place in places:
        if all([getattr(place, key) == value for key, value in data.items()]):
            places_list.append(place.to_dict())
    return jsonify(places_list)
