import model


class ValidationException(Exception):
    '''
    Abstract class for all validation exceptions
    '''

    def __init__(self, message):
        super().__init__(message)


class LocationValidationException(ValidationException):
    INCORRECT_FIELD_ERROR = 'Incorrect Amount of Fields'
    MISSING_LAT_FIELD_ERROR = 'Missing lat field'
    MISSING_LONG_FIELD_ERROR = 'Missing long field'
    INVALID_LAT_VALUE_ERROR = 'Invalid lat value'
    INVALID_LONG_VALUE_ERROR = 'Invalid long value'
    UNKNOWN_EXCEPTION = 'Invalid location format'

    def __init__(self, message):
        super().__init__(message)


class UpcValidationException(ValidationException):
    NOT_DIGITS_ERROR = 'Upc must be digits'
    INCORRECT_LENGTH_ERROR = 'Upc must have length 12'

    def __init__(self, message):
        super().__init__(message)


# location must have a lat in the range [-90,90] and a long in the range [-180,180]
def validate_location(loc):
    if len(loc) != 2:
        raise LocationValidationException(
            LocationValidationException.INCORRECT_FIELD_ERROR)
    if 'lat' not in loc:
        raise LocationValidationException(
            LocationValidationException.MISSING_LAT_FIELD_ERROR)
    if 'long' not in loc:
        raise LocationValidationException(
            LocationValidationException.MISSING_LONG_FIELD_ERROR)
    if loc['lat'] < -90 or loc['lat'] > 90:
        raise LocationValidationException(
            LocationValidationException.INVALID_LAT_VALUE_ERROR)
    if loc['long'] < -180 or loc['long'] > 180:
        raise LocationValidationException(
            LocationValidationException.INVALID_LONG_VALUE_ERROR)


# upc code must consist of 12 digits
def validate_upc(upc):
    if not upc.isdigit():
        raise UpcValidationException(UpcValidationException.NOT_DIGITS_ERROR)
    if len(upc) != 12:
        raise UpcValidationException(
            UpcValidationException.INCORRECT_LENGTH_ERROR)


# checks for the existence of all fields
def has_required(data, required):
    for field in required:
        if field not in data:
            return False

    return True


def is_valid_dir(dir):
    '''
    Ensures that vote direction is -1, 0, or 1
    '''
    return -1 <= dir and dir <= 1


def validate_unique_upc(upc):
    items = model.Item.objects(upc=upc)
    if len(items) == 0:
        return True
    return False
