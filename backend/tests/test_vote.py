import pytest
import json
import model
from utils import Error
import test_data
import validation


def test_upvote(client, existing_item):
    upc = str(existing_item.upc)
    store = existing_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    user = 'newuser'
    direction = 1

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    price = model.Item.objects(upc=upc).first().stores[0].prices[-1]
    assert user in price.upvotes


def test_downvote(client, existing_item):
    upc = str(existing_item.upc)
    store = existing_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    user = 'newuser'
    direction = -1

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    price = model.Item.objects(upc=upc).first().stores[0].prices[-1]
    assert user in price.downvotes


def test_undo_upvote(client, existing_item):
    upc = str(existing_item.upc)
    store = existing_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    user = 'newuser'
    direction = 1

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    price = model.Item.objects(upc=upc).first().stores[0].prices[-1]
    assert user in price.upvotes

    direction = 0

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    price = model.Item.objects(upc=upc).first().stores[0].prices[-1]
    assert not user in price.upvotes
    assert not user in price.downvotes


def test_undo_downvote(client, existing_item):
    upc = str(existing_item.upc)
    store = existing_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    user = 'newuser'
    direction = -1

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    price = model.Item.objects(upc=upc).first().stores[0].prices[-1]
    assert user in price.downvotes

    direction = 0

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    price = model.Item.objects(upc=upc).first().stores[0].prices[-1]
    assert not user in price.upvotes
    assert not user in price.downvotes


def test_upvote_then_downvote(client, existing_item):
    upc = str(existing_item.upc)
    store = existing_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    user = 'newuser'
    direction = 1

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    price = model.Item.objects(upc=upc).first().stores[0].prices[-1]
    assert user in price.upvotes

    direction = -1

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    price = model.Item.objects(upc=upc).first().stores[0].prices[-1]
    assert not user in price.upvotes
    assert user in price.downvotes


def test_downvote_then_upvote(client, existing_item):
    upc = str(existing_item.upc)
    store = existing_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    user = 'newuser'
    direction = -1

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    price = model.Item.objects(upc=upc).first().stores[0].prices[-1]
    assert user in price.downvotes

    direction = 1

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    price = model.Item.objects(upc=upc).first().stores[0].prices[-1]
    assert not user in price.downvotes
    assert user in price.upvotes


def test_invalid_unvote(client, existing_item):
    upc = str(existing_item.upc)
    store = existing_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    user = 'newuser'
    direction = 0

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': False, 'error': Error.NOT_VOTED.value}


def test_double_upvote(client, existing_item):
    upc = str(existing_item.upc)
    store = existing_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    user = 'newuser'
    direction = 1

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    price = model.Item.objects(upc=upc).first().stores[0].prices[-1]
    assert user in price.upvotes

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': False,
                        'error': Error.ALREADY_UPVOTED.value}


def test_double_downvote(client, existing_item):
    upc = str(existing_item.upc)
    store = existing_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    user = 'newuser'
    direction = -1

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': True, 'error': None}

    price = model.Item.objects(upc=upc).first().stores[0].prices[-1]
    assert user in price.downvotes

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': False,
                        'error': Error.ALREADY_DOWNVOTED.value}


def test_nonexistent_item(client, nonexistent_item):
    upc = str(nonexistent_item.upc)
    store = nonexistent_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    user = 'newuser'
    direction = 1

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': False, 'error': Error.ITEM_DNE.value}


def test_nonexistent_store(client, existing_item):
    upc = str(existing_item.upc)
    store = test_data.store10
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    user = 'newuser'
    direction = 1

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': False, 'error': Error.STORE_DNE.value}


def test_missing_direction(client, existing_item):
    upc = str(existing_item.upc)
    store = existing_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    user = 'newuser'

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg
    }))
    response = json.loads(rv.data)
    assert response == {'success': False,
                        'error': Error.MISSING_FIELDS.value}


def test_invalid_dir(client, existing_item):
    upc = str(existing_item.upc)
    store = existing_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    user = 'newuser'
    direction = 2

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response == {'success': False, 'error': Error.INVALID_DIR.value}


def test_invalid_user(client, existing_item):
    upc = str(existing_item.upc)
    store = existing_item.stores[0]
    store_name = str(store.name)
    lat = float(store.location['lat'])
    long_arg = float(store.location['long'])

    user = ''
    direction = 1

    rv = client.post('/vote', data=json.dumps({
        'upc': upc,
        'user': user,
        'store': store_name,
        'lat': lat,
        'long': long_arg,
        'dir': direction
    }))
    response = json.loads(rv.data)
    assert response['success'] == False
    assert 'ValidationError' in response['error']
    assert 'String value is too short' in response['error']
