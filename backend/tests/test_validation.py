import validation


# Location test

def test_valid_location():
    loc = {
        'lat': 0,
        'long': 0
    }
    validation.validate_location(loc)


def test_valid_location_edge_lat():
    loc = {
        'lat': 90,
        'long': 0
    }
    validation.validate_location(loc)


def test_valid_location_edge_long():
    loc = {
        'lat': 0,
        'long': 180
    }
    validation.validate_location(loc)


def test_invalid_location_too_many_fields():
    loc = {
        'lat': 0,
        'long': 0,
        'extra': 'peilun'
    }
    try:
        validation.validate_location(loc)
        assert False
    except:
        pass


def test_invalid_location_not_enough_fields():
    loc = {}
    try:
        validation.validate_location(loc)
        assert False
    except:
        pass


def test_invalid_location_lat():
    loc = {
        'lat': 1000,
        'long': 0
    }
    try:
        validation.validate_location(loc)
        assert False
    except:
        pass


def test_invalid_location_long():
    loc = {
        'lat': 0,
        'long': 1000
    }
    try:
        validation.validate_location(loc)
        assert False
    except:
        pass


# UPC test
def test_valid_upc():
    upc = '000000000000'
    validation.validate_upc(upc)


def test_invalid_upc_too_long():
    upc = '1234567890123'
    try:
        validation.validate_upc(upc)
        assert False
    except:
        pass


def test_invalid_upc_too_short():
    upc = '123'
    try:
        validation.validate_upc(upc)
        assert False
    except:
        pass


def test_invalid_upc_lowercase():
    upc = '00000000000a'
    try:
        validation.validate_upc(upc)
        assert False
    except:
        pass


def test_invalid_upc_uppercase():
    upc = '00000000000A'
    try:
        validation.validate_upc(upc)
        assert False
    except:
        pass


def test_invalid_upc_special():
    upc = '!@#$%^&*()_+'
    try:
        validation.validate_upc(upc)
        assert False
    except:
        pass


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
    assert validation.has_required(data, required_fields)


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
    assert validation.has_required(data, required_fields)


def test_invalid_has_required():
    data = {}
    assert not validation.has_required(data, required_fields)
