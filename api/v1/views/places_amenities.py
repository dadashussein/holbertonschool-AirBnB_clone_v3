#!/usr/bin/python3
"""places_amenities.py"""


from api.v1.views import app_views
from flask import abort, jsonify
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    """retrieves the list of all amenities of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = [obj.to_dict() for obj in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """ deletes an amenity from a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_amenity2(place_id, amenity_id):
    """ link an amenity to a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return (jsonify(amenity.to_dict()), 200)
    place.amenities.append(obj)
    storage.save()
    return (jsonify(amenity.to_dict(), 201))
