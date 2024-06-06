#!/usr/bin/python3
"""
flask app that runs the api
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def do_teardown(self):
    """
    closes the storage engine
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """
    handler for 404 page error
    """
    msg = {"error": "Not found"}
    return jsonify(msg), 404


if __name__ == "__main__":
    """
    runs the app when called from the command line
    """
    host = os.environ.get("HBNB_API_HOST")
    port = os.environ.get("HBNB_API_PORT")
    if not host:
        host = "0.0.0.0"
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
