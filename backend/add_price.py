from flask import Blueprint, request
import app
import validation
import model
import json
import mongoengine.errors

add_price_blueprint = Blueprint("add_price", __name__)


@add_price_blueprint.route('/price', methods=['POST'])
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
        return json.dumps({'success': False, 'error': app.Error.MISSING_FIELDS.value})

    item = model.Item.objects(upc=data['upc']).first()
    if item is None:
        return json.dumps({'success': False, 'error': app.Error.ITEM_DNE.value})

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
    except (validation.ValidationException, mongoengine.errors.ValidationError) as e:
        return json.dumps({'success': False, 'error': str(e)})

    return json.dumps({'success': True, 'error': None})
