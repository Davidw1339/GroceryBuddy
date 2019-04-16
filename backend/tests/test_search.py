import pytest
import json
import search
import test_data
import copy
from utils import Error


def test_no_args(client):
    rv = client.get('/search')
    response = json.loads(rv.data)
    assert response == {'success': False,
                        'error': Error.MISSING_KEYWORD_UPC.value}


def test_extra_args(client):
    rv = client.get('/search', data=json.dumps({
        'extra': 'peilun'
    }))
    response = json.loads(rv.data)
    assert response == {'success': False,
                        'error': Error.MISSING_KEYWORD_UPC.value}


def test_search_by_upc(client, existing_item):
    upc = str(existing_item.upc)

    rv = client.get('/search?upc=' + upc)
    response = json.loads(rv.data)
    first = response[0]

    assert first['upc'] == upc


def test_search_by_keyword_lower(client, existing_item):
    upc = str(existing_item.upc)
    name = str(existing_item.name).lower()

    rv = client.get('/search?keyword=' + name)
    response = json.loads(rv.data)
    first = response[0]

    assert first['upc'] == upc


def test_search_by_keyword_upper(client, existing_item):
    upc = str(existing_item.upc)
    name = str(existing_item.name).upper()

    rv = client.get('/search?keyword=' + name)
    response = json.loads(rv.data)
    first = response[0]

    assert first['upc'] == upc


def test_search_by_keyword_mixed(client, existing_item):
    upc = str(existing_item.upc)
    name = str(existing_item.name).lower()

    first = name[:int(len(name) / 2)].upper()
    second = name[int(len(name) / 2):]
    name = first + second

    rv = client.get('/search?keyword=' + name)
    response = json.loads(rv.data)
    first = response[0]

    assert first['upc'] == upc


def test_search_by_keyword_partial(client, existing_item):
    upc = str(existing_item.upc)
    name = str(existing_item.name).lower()

    name = name[:int(len(name) / 2)]

    rv = client.get('/search?keyword=' + name)
    response = json.loads(rv.data)
    first = response[0]

    assert first['upc'] == upc


def test_search_upc_over_keyword(client):
    first_item = copy.deepcopy(test_data.valid_items[0])
    first_item.save()
    first_upc = first_item.upc
    first_name = first_item.name

    second_item = copy.deepcopy(test_data.valid_items[1])
    second_item.save()
    second_upc = second_item.upc
    second_name = second_item.name

    assert first_upc != second_upc
    assert not first_name in second_name and not second_name in first_name

    rv = client.get(str.format(
        '/search?upc={}&keyword={}', first_upc, second_name))
    response = json.loads(rv.data)
    first_result = response[0]

    assert first_result['upc'] == first_upc


def test_invalid_limit(client, existing_item):
    name = str(existing_item.name).lower()

    rv = client.get('/search?keyword=' + name + '&limit=0')
    response = json.loads(rv.data)
    assert response == {'success': False,
                        'error': Error.INVALID_LIMIT.value}


def test_limit(client, db):
    keyword = 'test'
    limit = 1

    matches = []
    for i in test_data.valid_items:
        if keyword in i.name:
            copy.deepcopy(i).save()
            matches.append(i)
    matches = sorted(matches, key=lambda i: i.upc)

    rv = client.get('/search?keyword=' + keyword + '&limit=' + str(limit))
    response = json.loads(rv.data)
    assert len(response) == limit
    assert response[0]['upc'] == matches[0].upc
