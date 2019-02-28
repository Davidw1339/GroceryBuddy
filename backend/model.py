from mongoengine import EmbeddedDocument, StringField, IntField, DecimalField, DateTimeField, DictField, EmbeddedDocumentListField, Document
import validation


class Price(EmbeddedDocument):
    user = StringField(min_length=1, max_length=64)
    upvote = IntField(min_value=0)
    downvote = IntField(min_value=0)
    price = DecimalField(min_value=0, precision=2)
    date = DateTimeField()


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
    stores = EmbeddedDocumentListField(Store)
