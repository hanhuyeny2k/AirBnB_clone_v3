#!/usr/bin/python3
""" Create a new view for State objects that handles all default RestFul API"""
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


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves the list of all States"""
    items = []
    for obj in storage.all(State).values():
        items.append(obj.to_dict())
    return jsonify(items)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State object by id"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    else:
        ret = obj.to_dict()
        return jsonify(ret)


@app_views.route(
        '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ Delete a State object """
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Create a State """
    data = request.get_json()
    if data is None:
        abort(make_response("Not a JSON", 400))
    else:
        if "name" not in data.keys():
            abort(make_response("Missing name", 400))
        else:
            newstate = State(**data)
            storage.new(newstate)
            newstate.save()
            return jsonify(newstate.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Updates a State object """
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    else:
        data = request.get_json()
        keys_to_exclude = set(('id', 'created_at', 'updated_at'))
        dict2 = {k: v for k, v in data.items() if k not in keys_to_exclude}
        if data is None:
            abort(make_response("Not a JSON", 400))
        else:
            for k, v in dict2.items():
                setattr(obj, k, v)
            storage.save()
            return jsonify(obj.to_dict()), 200
