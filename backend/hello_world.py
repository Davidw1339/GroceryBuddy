from flask import Blueprint, request
import json
import validation
import mongoengine.errors
import model

hello_world_blueprint = Blueprint("hello_world", __name__)
HELLO_WORLD = 'Hello, Grocery buddies!'


@hello_world_blueprint.route('/', methods=['GET'])
def hello_world():
    return HELLO_WORLD
