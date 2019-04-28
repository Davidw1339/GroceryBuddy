from flask import Flask
from mongoengine import connect
from os import environ

from search import search_blueprint
from search_gps import search_gps_blueprint
from add_item import add_item_blueprint
from add_price import add_price_blueprint
from vote import vote_blueprint
from optimal_store import optimal_store_blueprint
from hello_world import hello_world_blueprint
from get_image import get_image_blueprint

# Create the Flask app and attach the logic for all routes.
app = Flask(__name__)
app.register_blueprint(search_blueprint)
app.register_blueprint(search_gps_blueprint)
app.register_blueprint(add_item_blueprint)
app.register_blueprint(add_price_blueprint)
app.register_blueprint(vote_blueprint)
app.register_blueprint(optimal_store_blueprint)
app.register_blueprint(hello_world_blueprint)
app.register_blueprint(get_image_blueprint)

# Connect to the database if the database URL
# is saved in an environment variable.
try:
    connect('grocery-db', host=environ['MONGO_HOST'])
except KeyError:
    pass


if __name__ == '__main__':
    # Start the Flask server
    app.run(host='0.0.0.0', port=80)
