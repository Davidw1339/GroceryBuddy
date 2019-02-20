from flask_mongoengine import MongoEngine

db = MongoEngine()


class Price(db.EmbeddedDocument):
    user = db.StringField()
    upvote = db.IntField()
    downvote = db.IntField()
    price = db.FloatField()
    date = db.DateTimeField()


class Store(db.EmbeddedDocument):
    name = db.StringField()
    location = db.DictField()
    price = db.EmbeddedDocumentListField(Price)


class Item(db.Document):
    meta = {'collection': 'grocery-items'}
    upc = db.StringField()
    name = db.StringField()
    stores = db.EmbeddedDocumentListField(Store)
