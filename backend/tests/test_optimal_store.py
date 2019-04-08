import pytest
import json
import model
from utils import Error
from test_data import valid_items
import copy


def test_invalid_upc(db, client):
    for item in valid_items:
        copy.deepcopy(item).save()
    result = model.Item.objects()

    upcs = ["000000000000"]
    for item in result:
        upcs.append(item.upc)

    rv = client.post('/optimal_store', data=json.dumps({
        'single_store': True,
        'items': upcs
    }))
    response = json.loads(rv.data)
    assert response['success'] is True
    assert response['error'] == Error.UPC_DNE.value
    assert len(response['optimal_prices']) == 1
    assert len(response['optimal_prices'][0]['upcs']) == (len(upcs) - 2)


def test_single_store(db, client):
    for item in valid_items:
        copy.deepcopy(item).save()
    result = model.Item.objects()

    upcs = []
    for item in result:
        upcs.append(item.upc)

    rv = client.post('/optimal_store', data=json.dumps({
        'single_store': True,
        'items': upcs
    }))
    response = json.loads(rv.data)
    assert response['success'] is True
    assert len(response['optimal_prices']) == 1
    assert len(response['optimal_prices'][0]['upcs']) == (len(upcs) - 1)


def test_multiple_stores(db, client):
    for item in valid_items:
        copy.deepcopy(item).save()
    result = model.Item.objects()

    upcs = []
    for item in result:
        upcs.append(item.upc)

    rv = client.post('/optimal_store', data=json.dumps({
        'single_store': False,
        'items': upcs
    }))
    response = json.loads(rv.data)
    assert response['success'] is True
    assert len(response['optimal_prices']) >= 1
    assert sum(len(dct['upcs'])
               for dct in response['optimal_prices']) == len(upcs)


def test_no_data(db, client):
    for item in valid_items:
        copy.deepcopy(item).save()

    rv = client.post('/optimal_store')
    response = json.loads(rv.data)
    assert response['success'] is False
    assert response['error'] == Error.INVALID_JSON.value
    assert response['optimal_prices'] is None


def test_no_items(db, client):
    for item in valid_items:
        copy.deepcopy(item).save()

    rv = client.post('/optimal_store', data=json.dumps({
        'single_store': True
    }))
    response = json.loads(rv.data)
    assert response['success'] is False
    assert response['error'] == Error.MISSING_UPC.value
    assert response['optimal_prices'] is None
