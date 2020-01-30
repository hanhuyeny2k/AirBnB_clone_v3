#!/usr/bin/python3
""" Create a new view for Amenities"""
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


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity objects"""
    items = []
    for obj in storage.all(Amenity).values():
        items.append(obj.to_dict())
    return jsonify(items)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a City object """
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    else:
        obj = obj.to_dict()
        return jsonify(obj)


@app_views.route(
        '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ Delete a Amenity object"""
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ Create an Amenity"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    else:
        if "name" not in data.keys():
            abort(400, "Missing name")
        else:
            new_amenity = Amenity(**data)
            new_amenity = new_amenity.to_dict()
            storage.save()
            return make_response(jsonify(new_amenity), 201)


@app_views.route('/amenity/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """ Updates a amenity object """
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    else:
        data = request.get_json()
        keys_to_exclude = set(('id', 'created_at', 'updated_at'))
        dict2 = {k: v for k, v in data.items() if k not in keys_to_exclude}
        if data is None:
            abort(400, "Not a JSON")
        else:
            obj = obj.to_dict()
            obj.update(dict2)
            return make_response(jsonify(obj), 200)
