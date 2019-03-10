from flask import Flask, request
import json
import model
import validation
from mongoengine import connect
from os import environ
from datetime import datetime
from enum import Enum


class Error(Enum):
    MISSING_FIELDS = 'Must fill all required fields'
    MISSING_KEYWORD_UPC = 'Request does not contain keyword or upc code'
    ITEM_DNE = 'Item does not exist in database'
    STORE_DNE = 'Store does not exist in database'
    INVALID_DIR = 'Invalid vote direction'
    ALREADY_UPVOTED = 'User has already upvoted'
    ALREADY_DOWNVOTED = 'User has already downvoted'
    NOT_VOTED = 'User has not voted, cannot undo'


class Vote(Enum):
    UP = 1
    NEUTRAL = 0
    DOWN = -1

    @classmethod
    def from_int(cls, i):
        mapping = {1: cls.UP, 0: cls.NEUTRAL, -1: cls.DOWN}
        return mapping[i]


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, Grocery buddies!'


@app.route('/item', methods=['POST'])
def post_item():
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
    except validation.ValidationException as e:
        return json.dumps({'success': False, 'error': str(e)})

    return json.dumps({'success': True, 'error': None})


@app.route('/price', methods=['POST'])
def add_price():
    '''
        Body: {"upc", "price", "user", "store", "lat", "long"}
        Response:
            - {"success": true or false},
            - {"error": error description}
    '''
    data = request.get_json(force=True)

    required_fields = ['upc', 'price', 'user', 'store', 'lat', 'long']
    if not validation.has_required(data, required_fields):
        return json.dumps({'success': False, 'error': Error.MISSING_FIELDS.value})

    item = model.Item.objects(upc=data['upc']).first()
    if item is None:
        return json.dumps({'success': False, 'error': Error.ITEM_DNE.value})

    new_price = model.Price(
        user=data['user'],
        upvotes=[],
        downvotes=[],
        price=data['price'],
        date=request.date
    )

    loc = {'lat': data['lat'], 'long': data['long']}
    store = item.stores.filter(name=data['store'], location=loc).first()
    if store is not None:
        store.prices.append(new_price)
    else:
        new_store = model.Store(
            name=data['store'],
            location=loc,
            prices=[new_price]
        )
        item.stores.append(new_store)

    try:
        item.save()
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)})

    return json.dumps({'success': True, 'error': None})


@app.route('/vote', methods=['POST'])
def vote():
    '''
        Body: {"upc", "user", "store", "lat", "long", "dir"}
        Response:
            - {"success": true or false},
            - {"error": error description}
    '''
    data = request.get_json(force=True)

    required_fields = ['upc', 'user', 'store', 'lat', 'long', 'dir']
    if not validation.has_required(data, required_fields):
        return json.dumps({'success': False, 'error': Error.MISSING_FIELDS.value})
    if not validation.is_valid_dir(data['dir']):
        return json.dumps({'success': False, 'error': Error.INVALID_DIR.value})

    direction = Vote.from_int(data['dir'])

    item = model.Item.objects(upc=data['upc']).first()
    if item is None:
        return json.dumps({'success': False, 'error': Error.ITEM_DNE.value})

    loc = {'lat': data['lat'], 'long': data['long']}
    store = item.stores.filter(name=data['store'], location=loc).first()
    if store is None:
        return json.dumps({'success': False, 'error': Error.STORE_DNE.value})
    else:
        price = store.prices[-1]
        if direction == Vote.UP:
            if data['user'] in price.upvotes:
                return json.dumps({'success': False, 'error': Error.ALREADY_UPVOTED.value})
            else:
                price.upvotes.append(data['user'])
            if data['user'] in price.downvotes:
                price.downvotes.remove(data['user'])
        elif direction == Vote.DOWN:
            if data['user'] in price.downvotes:
                return json.dumps({'success': False, 'error': Error.ALREADY_DOWNVOTED.value})
            else:
                price.downvotes.append(data['user'])
            if data['user'] in price.upvotes:
                price.upvotes.remove(data['user'])
        else:
            if data['user'] in price.upvotes:
                price.upvotes.remove(data['user'])
            elif data['user'] in price.downvotes:
                price.downvotes.remove(data['user'])
            else:
                return json.dumps({'success': False, 'error': Error.NOT_VOTED.value})

    try:
        item.save()
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)})

    return json.dumps({'success': True, 'error': None})


@app.route('/search', methods=['GET'])
def get_by_keyword():
    upc = request.args.get('upc')
    keyword = request.args.get('keyword')
    if upc:
        return model.Item.objects(upc=upc).to_json()
    elif keyword:
        return model.Item.objects(name__icontains=keyword).to_json()
    else:
        return json.dumps({'success': False, 'error': Error.MISSING_KEYWORD_UPC.value})


if __name__ == '__main__':
    connect('grocery-db', host=environ['MONGO_HOST'])
    app.run(host='0.0.0.0', port=80)
