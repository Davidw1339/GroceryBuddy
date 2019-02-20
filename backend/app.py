from flask import Flask, request
import json
import model
import config

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'grocery-db',
    'host': config.mongo_host
}
model.db.init_app(app)


@app.route('/')
def hello_world():
    return 'Hello, Grocery buddies!'


@app.route('/item', methods=['POST'])
def post_item():
    data = request.get_json(force=True)

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
    new_item.save()

    return json.dumps({'success': True, 'error': None})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
