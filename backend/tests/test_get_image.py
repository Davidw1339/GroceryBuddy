import pytest
import test_data
from utils import Error
import base64
import copy
import json


def test_get_valid_image(client, db):
    existing_item = copy.deepcopy(test_data.item13)
    existing_item.save()

    rv = client.get('/get_image?upc=' + existing_item.upc)
    assert rv.mimetype == 'image/jpeg'
    assert rv.data == bytes(existing_item.image)


def test_get_missing_image(client, existing_item):
    rv = client.get('/get_image?upc=' + existing_item.upc)
    response = json.loads(rv.data)
    assert response == {'success': False,
                        'error': Error.NO_IMAGE.value}


def test_get_nonexistent_upc(client, nonexistent_item):
    rv = client.get('/get_image?upc=' + nonexistent_item.upc)
    response = json.loads(rv.data)
    assert response == {'success': False,
                        'error': Error.ITEM_DNE.value}


def test_missing_field(client, existing_item):
    rv = client.get('/get_image?up=' + existing_item.upc)
    response = json.loads(rv.data)
    assert response == {'success': False,
                        'error': Error.MISSING_FIELDS.value}
