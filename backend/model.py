from mongoengine import (EmbeddedDocument, StringField, IntField, DecimalField,
                         DateTimeField, DictField, ListField, EmbeddedDocumentListField, Document)
import validation


class Price(EmbeddedDocument):
    user = StringField(min_length=1, max_length=64)
    upvotes = ListField(StringField(min_length=1, max_length=64))
    downvotes = ListField(StringField(min_length=1, max_length=64))
    price = DecimalField(min_value=0, precision=2)
    date = DecimalField(min_value=0, precision=6)


class Store(EmbeddedDocument):
    name = StringField(min_length=1, max_length=64)
    location = DictField()
    location.validate = validation.validate_location
    prices = EmbeddedDocumentListField(Price)


class Item(Document):
    meta = {'collection': 'grocery-items'}
    upc = StringField(max_length=12, min_length=12)
    upc.validate = validation.validate_upc
    name = StringField(min_length=1, max_length=64)
    image_url = StringField(min_length=0, max_length=512)
    stores = EmbeddedDocumentListField(Store)
