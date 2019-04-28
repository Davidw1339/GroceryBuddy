import test_data
from utils import Error
import base64
import copy
import json


def test_get_valid_image(client, db):
    '''
    Tests getting an image file for an item.
    '''
    existing_item = copy.deepcopy(test_data.item13)
    existing_item.save()

    rv = client.get('/get_image?upc=' + existing_item.upc)
    assert rv.mimetype == 'image/jpeg'
    assert rv.data == bytes(existing_item.image)


def test_get_missing_image(client, existing_item):
    '''
    Tests getting an image file for an item without an image.
    '''
    rv = client.get('/get_image?upc=' + existing_item.upc)
    response = json.loads(rv.data)
    assert response == {'success': False,
                        'error': Error.NO_IMAGE.value}


def test_get_nonexistent_upc(client, nonexistent_item):
    '''
    Tests getting an image file for a nonexistent item.
    '''
    rv = client.get('/get_image?upc=' + nonexistent_item.upc)
    response = json.loads(rv.data)
    assert response == {'success': False,
                        'error': Error.ITEM_DNE.value}


def test_missing_field(client, existing_item):
    '''
    Tests getting an image file without providing a UPC.
    '''
    rv = client.get('/get_image?up=' + existing_item.upc)
    response = json.loads(rv.data)
    assert response == {'success': False,
                        'error': Error.MISSING_FIELDS.value}
