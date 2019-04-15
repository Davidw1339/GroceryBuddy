import pytest
import json
import add_item
import model
import test_data
from utils import Error
import base64


def test_add_new_item(client, nonexistent_item, db):
    new_item = nonexistent_item
    name = str(new_item.name)
    upc = str(new_item.upc)

    store = new_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    price_data = store.prices[0]
    price = float(price_data.price)
    user = str(price_data.user)

    rv = client.post('/item', data=json.dumps({
        'name': name,
        'upc': upc,
        'price': price,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    new_item = model.Item.objects(
        upc=upc).first()
    assert str(new_item.name) == name
    new_store = new_item.stores[0]
    assert str(new_store.name) == store_name
    assert float(new_store.location['lat']) == lat
    assert float(new_store.location['long']) == long_arg
    new_price = new_store.prices[0]
    assert float(new_price.price) == price
    assert new_price.upvotes == []
    assert new_price.downvotes == []


def test_add_new_item_with_image_url(client, db):
    new_item = test_data.item8

    name = str(new_item.name)
    upc = str(new_item.upc)
    image_url = str(new_item.image_url)

    store = new_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    price_data = store.prices[0]
    price = float(price_data.price)
    user = str(price_data.user)

    rv = client.post('/item', data=json.dumps({
        'name': name,
        'upc': upc,
        'price': price,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'image_url': image_url
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    new_item = model.Item.objects(
        upc=upc).first()
    assert str(new_item.name) == name
    assert str(new_item.image_url) == image_url
    new_store = new_item.stores[0]
    assert str(new_store.name) == store_name
    assert float(new_store.location['lat']) == lat
    assert float(new_store.location['long']) == long_arg
    new_price = new_store.prices[0]
    assert float(new_price.price) == price
    assert new_price.upvotes == []
    assert new_price.downvotes == []


def test_add_new_item_with_image(client, db):
    new_item = test_data.item13

    name = str(new_item.name)
    upc = str(new_item.upc)
    image = str(base64.b64encode(new_item.image))

    store = new_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    price_data = store.prices[0]
    price = float(price_data.price)
    user = str(price_data.user)

    rv = client.post('/item', data=json.dumps({
        'name': name,
        'upc': upc,
        'price': price,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'image': image
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    new_item = model.Item.objects(
        upc=upc).first()
    assert str(new_item.name) == name
    new_store = new_item.stores[0]
    assert str(new_store.name) == store_name
    assert float(new_store.location['lat']) == lat
    assert float(new_store.location['long']) == long_arg
    new_price = new_store.prices[0]
    assert float(new_price.price) == price
    assert new_price.upvotes == []
    assert new_price.downvotes == []

    assert new_item.image is not None
    # Check substring in image_url
    assert new_item.image_url.find('/get_image?upc=' + new_item.upc) != -1


def test_add_new_item_image_over_url(client, db):
    '''
    Test that the image field has priority over image_url
    '''
    new_item = test_data.item13

    name = str(new_item.name)
    upc = str(new_item.upc)
    image = str(base64.b64encode(new_item.image))

    store = new_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    price_data = store.prices[0]
    price = float(price_data.price)
    user = str(price_data.user)

    rv = client.post('/item', data=json.dumps({
        'name': name,
        'upc': upc,
        'price': price,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'image': image,
        'image_url': 'Invalid URL'
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    new_item = model.Item.objects(
        upc=upc).first()
    assert str(new_item.name) == name
    new_store = new_item.stores[0]
    assert str(new_store.name) == store_name
    assert float(new_store.location['lat']) == lat
    assert float(new_store.location['long']) == long_arg
    new_price = new_store.prices[0]
    assert float(new_price.price) == price
    assert new_price.upvotes == []
    assert new_price.downvotes == []

    assert new_item.image is not None
    # Check substring in image_url
    assert new_item.image_url.find('/get_image?upc=' + new_item.upc) != -1


def test_existing_item(client, existing_item):
    name = str(existing_item.name)
    upc = str(existing_item.upc)

    store = existing_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    price_data = store.prices[0]
    price = float(price_data.price)
    user = str(price_data.user)

    rv = client.post('/item', data=json.dumps({
        'name': name,
        'upc': upc,
        'price': price,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg
    }))
    response = json.loads(rv.data)
    assert response == {'success': False,
                        'error': Error.ITEM_EXISTS.value}


def test_partial_item(client, nonexistent_item):
    new_item = nonexistent_item
    name = str(new_item.name)
    upc = str(new_item.upc)

    store = new_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    price_data = store.prices[0]
    price = float(price_data.price)

    rv = client.post('/item', data=json.dumps({
        'name': name,
        'upc': upc,
        'price': price,
        'store': store_name,
        'lat': lat,
        'long': long_arg
    }))
    response = json.loads(rv.data)
    assert response == {'success': False,
                        'error': Error.MISSING_FIELDS.value}


def test_invalid_price(client, nonexistent_item, db):
    new_item = nonexistent_item
    name = str(new_item.name)
    upc = str(new_item.upc)

    store = new_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    price_data = test_data.price6
    price = float(price_data.price)
    user = str(price_data.user)

    rv = client.post('/item', data=json.dumps({
        'name': name,
        'upc': upc,
        'price': price,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg
    }))
    response = json.loads(rv.data)
    assert response == {
        'success': False, 'error': "ValidationError (Item:None) (prices.price.Decimal value is too small: ['stores'])"}
