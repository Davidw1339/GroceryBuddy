from flask import Blueprint, request
import model
import json
import validation
from datetime import datetime
import mongoengine.errors
from utils import Error
import base64
from os import environ

add_item_blueprint = Blueprint("add_item", __name__)


def add_image(image_b64, item):
    '''
    Adds an image to the database.
    image_b64 should be a string of an image encoded in Base64.
    item should be the Item object to save under.
    '''
    raw_image = base64.b64decode(image_b64)
    item.image = raw_image

    try:
        base_url = environ['HOST_URL']
    except KeyError:
        # Default to localhost
        base_url = '127.0.0.1'
    item.image_url = base_url + '/get_image?upc=' + item.upc


@add_item_blueprint.route('/item', methods=['POST'])
def add_item():
    '''
    Adds a new item to the database.

    Body: {"name", "upc", "price", "user", "store", "lat", "long"[, "image", "image_url"]}
    Response:
        - {"success": true or false},
        - {"error": error description}
    '''
    data = request.get_json(force=True)

    required_fields = ['name', 'upc', 'price', 'user', 'store', 'lat', 'long']
    if not validation.has_required(data, required_fields):
        return json.dumps({'success': False, 'error': Error.MISSING_FIELDS.value})

    if not validation.validate_unique_upc(data['upc']):
        return json.dumps({'success': False, 'error': Error.ITEM_EXISTS.value})

    new_price = model.Price(
        user=data['user'],
        upvotes=[],
        downvotes=[],
        price=data['price'],
        date=datetime.now().timestamp()
    )
    new_store = model.Store(
        name=data['store'],
        location={
            'lat': data['lat'],
            'long': data['long']
        },
        prices=[new_price]
    )
    new_item = model.Item(
        upc=data['upc'],
        name=data['name'],
        image_url='',
        image=None,
        stores=[new_store]
    )

    if 'image' in data:
        add_image(data['image'], new_item)
    elif 'image_url' in data:
        new_item.image_url = data['image_url']

    try:
        new_item.save()
    except (validation.ValidationException, mongoengine.errors.ValidationError) as e:
        return json.dumps({'success': False, 'error': str(e)})

    return json.dumps({'success': True, 'error': None})
