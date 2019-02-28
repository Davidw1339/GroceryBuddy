from validation import *

def test_valid_location():
    loc = {
        'lat': 0,
        'long': 0
    }
    validate_location(loc)


def test_valid_location_edge_lat():
    loc = {
        'lat': 90,
        'long': 0
    }
    validate_location(loc)


def test_valid_location_edge_long():
    loc = {
        'lat': 0,
        'long': 180
    }
    validate_location(loc)


def test_invalid_location_too_many_fields():
    loc = {
        'lat': 0,
        'long': 0,
        'extra': 'peilun'
    }
    err_msg = None
    try:
        validate_location(loc)
    except LocationValidationException as e:
        err_msg=  e.__str__()
    assert err_msg == LocationValidationException.INCORRECT_FIELD_ERROR


def test_invalid_location_not_enough_fields():
    loc = {}
    err_msg = None
    try:
        validate_location(loc)
    except LocationValidationException as e:
        err_msg = e.__str__()
    assert err_msg == LocationValidationException.INCORRECT_FIELD_ERROR


def test_invalid_location_lat():
    loc = {
        'lat': 1000,
        'long': 0
    }
    err_msg = None
    try:
        validate_location(loc)
    except LocationValidationException as e:
         err_msg = e.__str__()
    assert err_msg == LocationValidationException.INVALID_LAT_VALUE_ERROR


def test_invalid_location_long():
    loc = {
        'lat': 0,
        'long': 1000
    }
    err_msg = None
    try:
        validate_location(loc)
    except LocationValidationException as e:
        err_msg = e.__str__()
    assert err_msg == LocationValidationException.INVALID_LONG_VALUE_ERROR


# UPC test
def test_valid_upc():
    upc = '000000000000'
    validate_upc(upc)


def test_invalid_upc_too_long():
    upc = '1234567890123'
    err_msg = None
    try:
        validate_upc(upc)
    except UpcValidationException as e:
        err_msg = e.__str__()
    assert err_msg == UpcValidationException.INCORRECT_LENGTH_ERROR


def test_invalid_upc_too_short():
    upc = '123'
    err_msg = None
    try:
        validate_upc(upc)
    except UpcValidationException as e:
        err_msg = e.__str__()
    assert err_msg == UpcValidationException.INCORRECT_LENGTH_ERROR


def test_invalid_upc_lowercase():
    upc = '00000000000a'
    err_msg = None
    try:
        validate_upc(upc)
    except UpcValidationException as e:
        err_msg = e.__str__()
    assert err_msg == UpcValidationException.NOT_DIGITS_ERROR


def test_invalid_upc_uppercase():
    upc = '00000000000A'
    err_msg = None
    try:
        validate_upc(upc)
    except UpcValidationException as e:
        err_msg = e.__str__()
    assert err_msg == UpcValidationException.NOT_DIGITS_ERROR


def test_invalid_upc_special():
    upc = '!@#$%^&*()_+'
    err_msg = None
    try:
        validate_upc(upc)
    except UpcValidationException as e:
        err_msg = e.__str__()
    assert err_msg == UpcValidationException.NOT_DIGITS_ERROR


required_fields = ['name', 'upc', 'price', 'user', 'store', 'lat', 'long']


def test_valid_has_required():
    data = {
        'name': None,
        'upc': None,
        'price': None,
        'user': None,
        'store': None,
        'lat': None,
        'long': None
    }
    assert has_required(data, required_fields)


def test_valid_has_required():
    data = {
        'name': None,
        'upc': None,
        'price': None,
        'user': None,
        'store': None,
        'lat': None,
        'long': None,
        'extra': None
    }
    assert has_required(data, required_fields)


def test_invalid_has_required():
    data = {}
    assert not has_required(data, required_fields)
