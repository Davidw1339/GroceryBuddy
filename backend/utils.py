from enum import Enum


class Error(Enum):
    '''
    An enum class that holds all custom errors and messages
    returned by this app.
    '''
    MISSING_FIELDS = 'Must fill all required fields'
    MISSING_KEYWORD_UPC = 'Request does not contain keyword or upc code'
    ITEM_EXISTS = 'Item already exists in database'
    ITEM_DNE = 'Item does not exist in database'
    STORE_DNE = 'Store does not exist in database'
    INVALID_DIR = 'Invalid vote direction'
    ALREADY_UPVOTED = 'User has already upvoted'
    ALREADY_DOWNVOTED = 'User has already downvoted'
    NOT_VOTED = 'User has not voted, cannot undo'
    INVALID_JSON = 'Could not parse JSON body'
    MISSING_UPC = 'No UPCs provided'
    UPC_DNE = 'Some UPCs provided were not found in the database'
    NO_IMAGE = 'No image uploaded for requested UPC'
    INVALID_LIMIT = 'Limit argument was not a positive integer'
    NO_ERROR = None
