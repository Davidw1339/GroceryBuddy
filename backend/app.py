from flask import Flask, request
import json
import model
import config
import validation
from mongoengine import connect

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'grocery-db',
    'host': config.mongo_host
}

connect(app.config['MONGODB_SETTINGS']['db'], host=config.mongo_host)


@app.route('/')
def hello_world():
    return 'Hello, Grocery buddies!'


@app.route('/item', methods=['POST'])
def post_item():
    """
        Body: {"name", "upc", "price", "user", "store", "lat", "long"}
        Response:
            - {"success": true or false},
            - {"error": error description}
    """
    data = request.get_json(force=True)

    required_fields = ['name', 'upc', 'price', 'user', 'store', 'lat', 'long']
    if not validation.has_required(data, required_fields):
        return json.dumps({'success': False, 'error': "Must fill all required fields"})

    new_price = model.Price(
        user=data['user'],
        upvote=0,
        downvote=0,
        price=data['price'],
        date=request.date
    )
    new_store = model.Store(
        name=data['store'],
        location={
            'lat': data['lat'],
            'long': data['long']
        },
        price=[new_price]
    )
    new_item = model.Item(
        upc=data['upc'],
        name=data['name'],
        stores=[new_store]
    )

    try:
        new_item.save()
    except Exception as e:
        return json.dumps({'success': False, 'error': str(e)})

    return json.dumps({'success': True, 'error': None})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
