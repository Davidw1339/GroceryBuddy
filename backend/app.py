from flask import Flask, request
import json
import model
import validation
from mongoengine import connect
import mongoengine.errors
from os import environ
from datetime import datetime
from enum import Enum

from search import search_blueprint
from add_item import add_item_blueprint
from add_price import add_price_blueprint
from vote import vote_blueprint
from optimal_store import optimal_store_blueprint
from hello_world import hello_world_blueprint


class Error(Enum):
    MISSING_FIELDS = 'Must fill all required fields'
    MISSING_KEYWORD_UPC = 'Request does not contain keyword or upc code'
    ITEM_EXISTS = 'Item already exists in database'
    ITEM_DNE = 'Item does not exist in database'
    STORE_DNE = 'Store does not exist in database'
    INVALID_DIR = 'Invalid vote direction'
    ALREADY_UPVOTED = 'User has already upvoted'
    ALREADY_DOWNVOTED = 'User has already downvoted'
    NOT_VOTED = 'User has not voted, cannot undo'
    INVALID_JSON = 'Could not parse JSON body'
    MISSING_UPC = 'No UPCs provided'
    UPC_DNE = 'Some UPCs provided were not found in the database'
    NO_ERROR = None


app = Flask(__name__)
app.register_blueprint(search_blueprint)
app.register_blueprint(add_item_blueprint)
app.register_blueprint(add_price_blueprint)
app.register_blueprint(vote_blueprint)
app.register_blueprint(optimal_store_blueprint)
app.register_blueprint(hello_world_blueprint)

try:
    connect('grocery-db', host=environ['MONGO_HOST'])
except KeyError:
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
