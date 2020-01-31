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


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieves the list of all User objects"""
    items = []
    for obj in storage.all(User).values():
        items.append(obj.to_dict())
    return jsonify(items)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object """
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    else:
        obj = obj.to_dict()
        return jsonify(obj)


@app_views.route(
        '/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Delete a user object"""
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Create a User"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    else:
        if "email" not in data.keys():
            abort(400, "Missing email")
        if "password" not in data.keys():
            abort(400, "Missing password")
        else:
            new_user = User(**data)
            storage.new(new_user)
            storage.save()
            return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ Updates a user object """
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    else:
        data = request.get_json()
        keys_to_exclude = set(('id', 'email', 'created_at', 'updated_at'))
        if data is None:
            abort(400, "Not a JSON")
        dict2 = {k: v for k, v in data.items() if k not in keys_to_exclude}
        for k, v in dict2.items():
            setattr(obj, k, v)
        storage.save()
        return make_response(jsonify(obj.to_dict), 200)
