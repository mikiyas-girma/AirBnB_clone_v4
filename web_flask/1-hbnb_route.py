#!/usr/bin/python3
"""starts flask application with two routes"""
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    """display hello hbnb"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """display hbnb"""
    return "HBNB"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
