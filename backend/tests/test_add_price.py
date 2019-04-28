import json
from utils import Error
import model
import test_data
import validation


def test_add_existing_store(client, existing_item):
    '''
    Tests updating the price of an item at a store
    that already has a price for it.
    '''
    upc = str(existing_item.upc)
    store = existing_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    price_data = test_data.valid_prices[5]
    price = float(price_data.price)
    user = str(price_data.user)

    num_existing_prices = len(store.prices)

    rv = client.post('/price', data=json.dumps({
        'upc': upc,
        'price': price,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    new_price = model.Item.objects(
        upc=upc).first().stores[0].prices[num_existing_prices]
    assert float(new_price.price) == price
    assert new_price.upvotes == []
    assert new_price.downvotes == []


def test_add_new_store(client, existing_item):
    '''
    Tests adding a price for an item at a new store.
    '''
    upc = str(existing_item.upc)
    new_store = test_data.store10
    store_name = str(new_store.name)
    lat = float(new_store.location['lat'])
    long_arg = float(new_store.location['long'])

    price_data = test_data.valid_prices[5]
    price = float(price_data.price)
    user = str(price_data.user)

    rv = client.post('/price', data=json.dumps({
        'upc': upc,
        'price': price,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    loc = {'lat': lat, 'long': long_arg}
    new_price = model.Item.objects(upc=upc).first().stores.filter(
        name=store_name, location=loc).first().prices[0]
    assert float(new_price.price) == price
    assert new_price.upvotes == []
    assert new_price.downvotes == []


def test_nonexistent_item(client, nonexistent_item):
    '''
    Tests adding a price for a nonexistent item.
    '''
    upc = str(nonexistent_item.upc)
    store = nonexistent_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    price_data = test_data.valid_prices[5]
    price = float(price_data.price)
    user = str(price_data.user)

    rv = client.post('/price', data=json.dumps({
        'upc': upc,
        'price': price,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg
    }))
    response = json.loads(rv.data)
    assert response == {'success': False, 'error': Error.ITEM_DNE.value}


def test_missing_user(client, existing_item):
    '''
    Tests adding a price without a user.
    '''
    upc = str(existing_item.upc)
    store = existing_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    price_data = test_data.valid_prices[5]
    price = float(price_data.price)

    rv = client.post('/price', data=json.dumps({
        'upc': upc,
        'price': price,
        'store': store_name,
        'lat': lat,
        'long': long_arg
    }))
    response = json.loads(rv.data)
    assert response == {'success': False,
                        'error': Error.MISSING_FIELDS.value}


def test_add_invalid_store(client, existing_item):
    '''
    Tests adding a price for an item to a store with invalid location.
    '''
    upc = str(existing_item.upc)
    new_store = test_data.store5
    store_name = str(new_store.name)
    lat = float(new_store.location['lat'])
    long_arg = float(new_store.location['long'])

    price_data = test_data.valid_prices[5]
    price = float(price_data.price)
    user = str(price_data.user)

    rv = client.post('/price', data=json.dumps({
        'upc': upc,
        'price': price,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg
    }))
    response = json.loads(rv.data)
    assert response == {
        'success': False, 'error': validation.LocationValidationException.INVALID_LAT_VALUE_ERROR}
