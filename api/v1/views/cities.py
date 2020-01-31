#!/usr/bin/python3
"""class for city http methods"""
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


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_cities_from_state(state_id):
        """retrive cities from given state"""
        items = []
        if request.method == "GET":
                obj = storage.get("State", state_id)
                for item in obj.cities.values():
                        if item.state_id == state_id:
                                items.append(item.to_dict())
                return jsonify(items)
        elif request.method == 'POST':
                obj = storage.get("State", state_id)
                data = request.get_json()
                if not obj:
                        abort(404)
                if data is None:
                        abort(400, "Not a JSON")
                if "name" not in data.keys():
                        abort(400, "Missing name")
                else:
                        data['state_id'] = state_id
                        newcity = City(**data)
                        storage.new(newcity)
                        storage.save()
                return make_response(jsonify(newcity.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_cities(city_id):
    """retrive city by id"""
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    else:
        ret = obj.to_dict()
        return jsonify(ret)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """delete city by id"""
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
        """update city object"""
        obj = storage.get("City", city_id)
        if obj is None:
                abort(404)
        else:
            data = request.get_json()
            keys_to_exclude = set(('id', 'created_at', 'updated_at'))
            dict2 = {k: v for k, v in data.items() if k not in keys_to_exclude}
            if data is None:
                    abort(400, "Not a JSON")
            else:
                for k, v in dict2.items():
                        setattr(obj, k, v)
                storage.save()
                return make_response(jsonify(obj.to_dict()), 200)
