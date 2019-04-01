import pytest
import json
import add_item
import model
import test_data


def test_add_new_item(client, nonexistent_item):
    name = str(nonexistent_item.name)
    upc = str(nonexistent_item.upc)

    store = nonexistent_item.stores[0]
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


def test_add_new_item_with_image(client):
    nonexistent_item = test_data.item8
    assert model.Item.objects(upc=nonexistent_item.upc).count(
    ) == 0, 'Test item was not cleared from database after previous test'

    name = str(nonexistent_item.name)
    upc = str(nonexistent_item.upc)
    image_url = str(nonexistent_item.image_url)

    store = nonexistent_item.stores[0]
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
    assert response == {'success': False, 'error': add_item.Error.ITEM_EXISTS.value}


def test_partial_item(client, nonexistent_item):
    name = str(nonexistent_item.name)
    upc = str(nonexistent_item.upc)

    store = nonexistent_item.stores[0]
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
                        'error': add_item.Error.MISSING_FIELDS.value}


def test_invalid_price(client, nonexistent_item):
    name = str(nonexistent_item.name)
    upc = str(nonexistent_item.upc)

    store = nonexistent_item.stores[0]
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
