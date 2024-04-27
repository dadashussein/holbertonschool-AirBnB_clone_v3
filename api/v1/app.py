#!/usr/bin/python3
""" Starts a Flask web application """

from api.v1.views import app_views
from flask import Flask
from models import storage
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Closes the storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """404 page"""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=int(port), threaded=True)
