from flask import Blueprint

hello_world_blueprint = Blueprint("hello_world", __name__)
HELLO_WORLD = 'Hello, Grocery buddies!'


@hello_world_blueprint.route('/', methods=['GET'])
def hello_world():
    '''
    Returns a constant string to demonstrate
    that the server is responsive.
    '''
    return HELLO_WORLD
