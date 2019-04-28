import model


class ValidationException(Exception):
    '''
    Abstract class for all validation exceptions.
    '''

    def __init__(self, message):
        '''
        Initializes base class with error message.
        '''
        super().__init__(message)


class LocationValidationException(ValidationException):
    '''
    Exception class for invalid locations.
    '''
    INCORRECT_FIELD_ERROR = 'Incorrect Amount of Fields'
    MISSING_LAT_FIELD_ERROR = 'Missing lat field'
    MISSING_LONG_FIELD_ERROR = 'Missing long field'
    INVALID_LAT_VALUE_ERROR = 'Invalid lat value'
    INVALID_LONG_VALUE_ERROR = 'Invalid long value'
    UNKNOWN_EXCEPTION = 'Invalid location format'

    def __init__(self, message):
        '''
        Initializes base class with error message.
        '''
        super().__init__(message)


class UpcValidationException(ValidationException):
    '''
    Exception class for invalid UPCs.
    '''
    NOT_DIGITS_ERROR = 'Upc must be digits'
    INCORRECT_LENGTH_ERROR = 'Upc must have length 12'

    def __init__(self, message):
        '''
        Initializes base class with error message.
        '''
        super().__init__(message)


def validate_location(loc):
    '''
    Checks that latitude is in the range [-90, 90]
    and longitude is in the range [-180, 180].
    '''
    if len(loc) != 2:
        raise LocationValidationException(
            LocationValidationException.INCORRECT_FIELD_ERROR)
    if 'lat' not in loc:
        raise LocationValidationException(
            LocationValidationException.MISSING_LAT_FIELD_ERROR)
    if 'long' not in loc:
        raise LocationValidationException(
            LocationValidationException.MISSING_LONG_FIELD_ERROR)
    if ((type(loc['lat']) is not float and type(loc['lat']) is not int)
            or loc['lat'] < -90 or loc['lat'] > 90):
        raise LocationValidationException(
            LocationValidationException.INVALID_LAT_VALUE_ERROR)
    if ((type(loc['long']) is not float and type(loc['long']) is not int)
            or loc['long'] < -180 or loc['long'] > 180):
        raise LocationValidationException(
            LocationValidationException.INVALID_LONG_VALUE_ERROR)


def validate_upc(upc):
    '''
    Checks that a UPC has 12 numeric digits.
    '''
    if not upc.isdigit():
        raise UpcValidationException(UpcValidationException.NOT_DIGITS_ERROR)
    if len(upc) != 12:
        raise UpcValidationException(
            UpcValidationException.INCORRECT_LENGTH_ERROR)


def has_required(data, required):
    '''
    Checks that all required fields are given.
    '''
    for field in required:
        if field not in data:
            return False

    return True


def is_valid_dir(dir):
    '''
    Checks that vote direction is -1, 0, or 1.
    '''
    return -1 <= dir and dir <= 1


def validate_unique_upc(upc):
    '''
    Checks that a UPC does not already exist in the database.
    '''
    items = model.Item.objects(upc=upc)
    if len(items) == 0:
        return True
    return False
