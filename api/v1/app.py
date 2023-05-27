#!/usr/bin/python3
'''app module'''
from models import storage
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def close(exception):
    '''close session'''
    storage.close()


@app.errorhandler(404)
def error_404(e):
    '''Handles error 404'''
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    from os import getenv

    h = getenv('HBNB_API_HOST') or '0.0.0.0'
    p = getenv('HBNB_API_PORT') or 5000
    app.run(host=h, port=p, threaded=True)
