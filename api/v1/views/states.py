#!/usr/bin/python3

from flask import Flask
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



@app_views.route('/states', methods=['GET'])
def get_states():
	items = []
	for obj in storage.all(State).values():
		items.append(obj.to_dict())
	return str(items)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    else:
        ret = obj.to_dict()
        return (str(ret))


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
