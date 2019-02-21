

# location must have a lat in the range [-90,90] and a long in the range [-180,180]
def validate_location(loc):
    try:
        if len(loc) != 2:
            raise Exception()
        if 'lat' not in loc or 'long' not in loc:
            raise Exception()
        if loc['lat'] < -90 or loc['lat'] > 90 or loc['long'] < -180 or loc['long'] > 180:
            raise Exception()
    except Exception:
        raise Exception('Invalid location format')


# upc code must consist of 12 digits
def validate_upc(upc):
    try:
        if len(upc) != 12 or not upc.isdigit():
            raise Exception()
    except Exception:
        raise Exception('Invalid upc code')


# checks for the existence of all fields
def has_required(data, required):
    for field in required:
        if field not in data:
            return False

    return True
