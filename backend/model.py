from mongoengine import (EmbeddedDocument, StringField, DecimalField,
                         BinaryField, DictField, ListField,
                         EmbeddedDocumentListField, Document)
import validation


class Price(EmbeddedDocument):
    '''
    Holds the data related to a specific price of an item
    at a specific store.
    '''
    user = StringField(min_length=1, max_length=64, required=True)
    upvotes = ListField(StringField(min_length=1, max_length=64))
    downvotes = ListField(StringField(min_length=1, max_length=64))
    price = DecimalField(min_value=0, precision=2, required=True)
    date = DecimalField(min_value=0, precision=6, required=True)


class Store(EmbeddedDocument):
    '''
    Holds the data related to a specific store for an item.
    '''
    name = StringField(min_length=1, max_length=64, required=True)
    location = DictField(required=True)
    location.validate = validation.validate_location
    prices = EmbeddedDocumentListField(Price, required=True)


class Item(Document):
    '''
    Holds the data related to an item.
    '''
    meta = {'collection': 'grocery-items'}
    upc = StringField(max_length=12, min_length=12, required=True)
    upc.validate = validation.validate_upc
    name = StringField(min_length=1, max_length=64, required=True)
    image_url = StringField(min_length=0, max_length=512)
    image = BinaryField()
    stores = EmbeddedDocumentListField(Store, required=True)
