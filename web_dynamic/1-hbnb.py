#!/usr/bin/python3
"""
script that starts flask web application
"""
import uuid
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_session(exec):
    """
    close session
    """
    storage.close()


@app.route('/1-hbnb')
def hbnb():
    """
    display hbnb
    """
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    return render_template('1-hbnb.html',
                           states=states,
                           amenities=amenities,
                           places=places,
                           cache_id=uuid.uuid4())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
