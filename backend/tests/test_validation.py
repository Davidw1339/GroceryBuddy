from validation import *


def test_valid_location():
    '''
    Tests validation of a valid location.
    '''
    loc = {
        'lat': 0,
        'long': 0
    }
    validate_location(loc)


def test_valid_location_edge_lat():
    '''
    Tests validation of a valid location.
    '''
    loc = {
        'lat': 90,
        'long': 0
    }
    validate_location(loc)


def test_valid_location_edge_long():
    '''
    Tests validation of a valid location.
    '''
    loc = {
        'lat': 0,
        'long': 180
    }
    validate_location(loc)


def test_invalid_location_too_many_fields():
    '''
    Tests validation of a location with too many fields.
    '''
    loc = {
        'lat': 0,
        'long': 0,
        'extra': 'peilun'
    }
    err_msg = None
    try:
        validate_location(loc)
    except LocationValidationException as e:
        err_msg = e.__str__()
    assert err_msg == LocationValidationException.INCORRECT_FIELD_ERROR


def test_invalid_location_not_enough_fields():
    '''
    Tests validation of a location with missing fields.
    '''
    loc = {}
    err_msg = None
    try:
        validate_location(loc)
    except LocationValidationException as e:
        err_msg = e.__str__()
    assert err_msg == LocationValidationException.INCORRECT_FIELD_ERROR


def test_invalid_location_lat():
    '''
    Tests validation of an invalid latitude.
    '''
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
    '''
    Tests validation of an invalid longitude.
    '''
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


def test_missing_lat():
    '''
    Tests validation of a missing latitude.
    '''
    loc = {
        'latt': 0,
        'long': 90
    }
    err_msg = None
    try:
        validate_location(loc)
    except LocationValidationException as e:
        err_msg = e.__str__()
    assert err_msg == LocationValidationException.MISSING_LAT_FIELD_ERROR


def test_missing_long():
    '''
    Tests validation of a missing longitude.
    '''
    loc = {
        'lat': 0,
        'lon': 90
    }
    err_msg = None
    try:
        validate_location(loc)
    except LocationValidationException as e:
        err_msg = e.__str__()
    assert err_msg == LocationValidationException.MISSING_LONG_FIELD_ERROR


# UPC test
def test_valid_upc():
    '''
    Tests validation of a valid UPC.
    '''
    upc = '000000000000'
    validate_upc(upc)


def test_invalid_upc_too_long():
    '''
    Tests validation of a UPC that is too long.
    '''
    upc = '1234567890123'
    err_msg = None
    try:
        validate_upc(upc)
    except UpcValidationException as e:
        err_msg = e.__str__()
    assert err_msg == UpcValidationException.INCORRECT_LENGTH_ERROR


def test_invalid_upc_too_short():
    '''
    Tests validation of a UPC that is too short.
    '''
    upc = '123'
    err_msg = None
    try:
        validate_upc(upc)
    except UpcValidationException as e:
        err_msg = e.__str__()
    assert err_msg == UpcValidationException.INCORRECT_LENGTH_ERROR


def test_invalid_upc_lowercase():
    '''
    Tests validation of a UPC with letters.
    '''
    upc = '00000000000a'
    err_msg = None
    try:
        validate_upc(upc)
    except UpcValidationException as e:
        err_msg = e.__str__()
    assert err_msg == UpcValidationException.NOT_DIGITS_ERROR


def test_invalid_upc_uppercase():
    '''
    Tests validation of a UPC with letters.
    '''
    upc = '00000000000A'
    err_msg = None
    try:
        validate_upc(upc)
    except UpcValidationException as e:
        err_msg = e.__str__()
    assert err_msg == UpcValidationException.NOT_DIGITS_ERROR


def test_invalid_upc_special():
    '''
    Tests validation of a UPC with special characters.
    '''
    upc = '!@#$%^&*()_+'
    err_msg = None
    try:
        validate_upc(upc)
    except UpcValidationException as e:
        err_msg = e.__str__()
    assert err_msg == UpcValidationException.NOT_DIGITS_ERROR


def test_upc_exists(existing_item):
    '''
    Tests validation of UPC uniqueness for a duplicate UPC.
    '''
    upc = str(existing_item.upc)
    assert validate_unique_upc(upc) is False


def test_upc_does_not_exist(nonexistent_item):
    '''
    Tests validation of UPC uniqueness for a new UPC.
    '''
    upc = str(nonexistent_item.upc)
    assert validate_unique_upc(upc) is True


required_fields = ['name', 'upc', 'price', 'user', 'store', 'lat', 'long']


def test_valid_has_required():
    '''
    Tests validation of fields for valid fields.
    '''
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


def test_valid_has_required_extra():
    '''
    Tests validation of fields for valid fields and extra fields.
    '''
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
    '''
    Tests validation of fields for missing fields.
    '''
    data = {}
    assert not has_required(data, required_fields)
