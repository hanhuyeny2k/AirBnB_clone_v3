#!/usr/bin/python3
""" Create a new view for User"""
from flask import Flask, request
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import jsonify, abort, make_response
from api.v1.views import app_views
import json
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Place objects in a city"""
    items = []
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    for obj in storage.all(Place).values():
        if obj.city_id == city_id:
            items.append(obj.to_dict())
    return jsonify(items)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    else:
        obj = obj.to_dict()
        return jsonify(obj)


@app_views.route(
        '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ Delete a place object"""
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """ Create a Place"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    else:
        if "user_id" not in data.keys():
            abort(400, "Missing user_id")
        test = storage.get("User", data['user_id'])
        if not test:
            abort(404)
        if "name" not in data.keys():
            abort(400, "Missing name")
        else:
            new_place = Place(**data)
            storage.new(new_place)
            storage.save()
            return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ Updates a place object """
    obj = storage.get("Place", place_id)
    if obj is None:
        abort(404)
    else:
        data = request.get_json()
        keys_to_exclude = set((
            'id', 'user_id', 'city_id', 'created_at', 'updated_at'))
        if data is None:
            abort(400, "Not a JSON")
        dict2 = {k: v for k, v in data.items() if k not in keys_to_exclude}
        for k, v in dict2.items():
            setattr(obj, k, v)
        storage.save()
        obj = obj.to_dict()
        return make_response(jsonify(obj), 200)
