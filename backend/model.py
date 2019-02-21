from flask_mongoengine import MongoEngine
import validation

db = MongoEngine()


class Price(db.EmbeddedDocument):
    user = db.StringField(min_length=1, max_length=64)
    upvote = db.IntField(min_value=0)
    downvote = db.IntField(min_value=0)
    price = db.DecimalField(min_value=0, precision=2)
    date = db.DateTimeField()


class Store(db.EmbeddedDocument):
    name = db.StringField(min_length=1, max_length=64)
    location = db.DictField()
    location.validate = validation.validate_location
    price = db.EmbeddedDocumentListField(Price)


class Item(db.Document):
    meta = {'collection': 'grocery-items'}
    upc = db.StringField(max_length=12, min_length=12)
    upc.validate = validation.validate_upc
    name = db.StringField(min_length=1, max_length=64)
    stores = db.EmbeddedDocumentListField(Store)
