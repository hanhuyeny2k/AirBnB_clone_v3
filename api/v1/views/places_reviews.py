#!/usr/bin/python3
""" Create a new view for Reviews"""
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


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """ Retrieves the list of all Review objects of a Place"""
    items = []
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    for obj in storage.all(Place).values():
        if obj.place_id == place_id:
            items.append(obj.to_dict())
    return jsonify(items)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(place_id):
    """ Retrieves a Review object """
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    else:
        obj = obj.to_dict()
        return jsonify(obj)


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(place_id):
    """ Delete a place object"""
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """ Create a Reviews"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    else:
        if "user_id" not in data.keys():
            abort(400, "Missing user_id")
        test = storage.get("User", data['user_id'])
        if not test:
            abort(404)
        if "text" not in data.keys():
            abort(400, "Missing text")
        else:
            new_review = Review(**data)
            storage.new(new_review)
            storage.save()
            return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """ Updates a review object """
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    else:
        data = request.get_json()
        keys_to_exclude = set((
            'id', 'user_id', 'place_id', 'created_at', 'updated_at'))
        dict2 = {k: v for k, v in data.items() if k not in keys_to_exclude}
        if data is None:
            abort(400, "Not a JSON")
        else:
            for k, v in dict2.items():
                setattr(obj, k, v)
            storage.save()
            obj = obj.to_dict()
            return make_response(jsonify(obj), 200)
