#!/usr/bin/python3
""" a script that starts a Flask web application """

from flask import Flask
from flask import render_template
from models.state import State
from models.amenity import Amenity
from models.user import User
from models import storage

app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb_main():
    """get the states and amenities lists"""
    states = storage.all(State)
    amenities = storage.all(Amenity)
    places = storage.all(Place)
    return render_template("100-hbnb.html",
                           states=states.values(),
                           amenities=amenities.values(),
                           places=places.values())


@app.teardown_appcontext
def teardown_appcontext(exception=None):
    """close the storage session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
