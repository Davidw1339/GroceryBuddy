from flask import Flask, request
import json
import model
import validation
from mongoengine import connect
import mongoengine.errors
from os import environ
from datetime import datetime

from search import search_blueprint
from search_gps import search_gps_blueprint
from add_item import add_item_blueprint
from add_price import add_price_blueprint
from vote import vote_blueprint
from optimal_store import optimal_store_blueprint
from hello_world import hello_world_blueprint
from get_image import get_image_blueprint


app = Flask(__name__)
app.register_blueprint(search_blueprint)
app.register_blueprint(search_gps_blueprint)
app.register_blueprint(add_item_blueprint)
app.register_blueprint(add_price_blueprint)
app.register_blueprint(vote_blueprint)
app.register_blueprint(optimal_store_blueprint)
app.register_blueprint(hello_world_blueprint)
app.register_blueprint(get_image_blueprint)

try:
    connect('grocery-db', host=environ['MONGO_HOST'])
except KeyError:
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
