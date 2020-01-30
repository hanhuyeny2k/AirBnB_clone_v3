#!/usr/bin/python3
"""api for hbnb project(airbnb clone)"""
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(x):
    """close storage after session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    HBNB_API_HOST = '0.0.0.0'
    HBNB_API_PORT = '5000'
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
