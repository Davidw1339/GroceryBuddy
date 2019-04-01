from flask import Blueprint, request
from enum import Enum
import model
import json
import validation
from datetime import datetime
import mongoengine.errors

add_item_blueprint = Blueprint("add_item", __name__)

class Error(Enum):
    MISSING_FIELDS = 'Must fill all required fields'
    ITEM_EXISTS = 'Item already exists in database'

@add_item_blueprint.route('/item', methods=['POST'])
def add_item():
    '''
        Body: {"name", "upc", "price", "user", "store", "lat", "long"[, "image_url"]}
        Response:
            - {"success": true or false},
            - {"error": error description}
    '''
    data = request.get_json(force=True)

    required_fields = ['name', 'upc', 'price', 'user', 'store', 'lat', 'long']
    if not validation.has_required(data, required_fields):
        return json.dumps({'success': False, 'error': Error.MISSING_FIELDS.value})

    lookup = model.Item.objects(upc=data['upc']).first()
    if lookup is not None:
        return json.dumps({'success': False, 'error': Error.ITEM_EXISTS.value})

    if 'image_url' in data:
        image_url = data['image_url']
    else:
        image_url = ''

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
        image_url=image_url,
        stores=[new_store]
    )

    try:
        new_item.save()
    except (validation.ValidationException, mongoengine.errors.ValidationError) as e:
        return json.dumps({'success': False, 'error': str(e)})

    return json.dumps({'success': True, 'error': None})