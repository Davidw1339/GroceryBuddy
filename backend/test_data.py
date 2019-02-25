import model
import random
import string
from datetime import datetime

# valid
price0 = model.Price(
    user='admin',
    upvote=10,
    downvote=5,
    price=1.99,
    date=datetime.now()
)

# valid
price1 = model.Price(
    user='admin',
    upvote=7,
    downvote=4,
    price=0.99,
    date=datetime.now()
)

# valid
price2 = model.Price(
    user='admin',
    upvote=0,
    downvote=0,
    price=0.00,
    date=datetime.now()
)

# valid
price3 = model.Price(
    user='admin',
    upvote=200,
    downvote=1000,
    price=139.99,
    date=datetime.now()
)

# valid
price4 = model.Price(
    user='admin',
    upvote=20,
    downvote=19,
    price=12.89,
    date=datetime.now()
)

# array of valid prices
valid_prices = [
    price0,
    price1,
    price2,
    price3,
    price4,
]

# user: empty string
price5 = model.Price(
    user='',
    upvote=10,
    downvote=5,
    price=1.99,
    date=datetime.now()
)

# upvote: negative upvote
price6 = model.Price(
    user='admin',
    upvote=-7,
    downvote=4,
    price=0.99,
    date=datetime.now()
)

# downvote: negative downvote
price7 = model.Price(
    user='admin',
    upvote=0,
    downvote=-1,
    price=0.00,
    date=datetime.now()
)

# price: negative price
price8 = model.Price(
    user='admin',
    upvote=200,
    downvote=1000,
    price=-139.99,
    date=datetime.now()
)

# none fields
price9 = model.Price(
    user=None,
    upvote=None,
    downvote=None,
    price=None,
    date=datetime.now()
)

# price: too many digits in cents
price10 = model.Price(
    user='admin',
    upvote=200,
    downvote=100,
    price=19.999,
    date=datetime.now()
)

# array of invalid prices
invalid_prices = [
    price5,
    price6,
    price7,
    price8,
    price9,
    price10,
]

# valid
store0 = model.Store(
    name='Walmart',
    location={
        'lat': 0,
        'long': 0
    },
    price=[price0, price1]
)

# valid
store1 = model.Store(
    name='County Market',
    location={
        'lat': 0,
        'long': 0
    },
    price=valid_prices
)

# valid
store2 = model.Store(
    name='Target',
    location={
        'lat': 0,
        'long': 0
    },
    price=random.shuffle(valid_prices)
)

# valid
store3 = model.Store(
    name='Meijer',
    location={
        'lat': 0,
        'long': 0
    },
    price=[
        price0,
        price2,
        price1,
    ]
)

# array of valid stores
valid_stores = [
    store0,
    store1,
    store2,
    store3,
]

# name: name too long
store4 = model.Store(
    name=(''.join(random.choices(string.ascii_letters + string.digits, k=65))),
    location={
        'lat': 0,
        'long': 0
    },
    price=[
        price1,
        price3,
        price0,
        price2,
        price4,
    ]
)

# location: invalid lat
store5 = model.Store(
    name='Target',
    location={
        'lat': 1000,
        'long': 0
    },
    price=[
        price1,
        price3,
    ]
)

# location: invalid long
store6 = model.Store(
    name='Meijer',
    location={
        'lat': 0,
        'long': 1000
    },
    price=[
        price2,
        price0,
    ]
)

# location: extra field
store7 = model.Store(
    name='Walmart',
    location={
        'lat': 0,
        'lat': 0,
        'rand': None
    },
    price=[
        price1,
        price4,
    ]
)

# price: invalid price array
store8 = model.Store(
    name='Target',
    location={
        'lat': 0,
        'long': 0
    },
    price=invalid_prices
)

# empty fields
store9 = model.Store(
    name=None,
    location=None,
    price=None
)

invalid_stores = [
    store4,
    store5,
    store6,
    store7,
    store8,
    store9,
]

item0 = model.Item(
    name='apple',
    upc='042100005264',
    stores=valid_stores
)

item1 = model.Item(
    name='milk',
    upc=(''.join(random.choices(string.digits, k=12))),
    stores=random.shuffle(valid_stores)
)

valid_items = [
    item0,
    item1,
]

# name: too many characters
item2 = model.Item(
    name=(''.join(random.choices(string.ascii_letters, k=65))),
    upc=(''.join(random.choices(string.digits, k=12))),
    stores=random.shuffle(valid_stores)
)

# upc: too short
item3 = model.Item(
    name=(''.join(random.choices(string.ascii_letters, k=32))),
    upc=(''.join(random.choices(string.digits, k=10))),
    stores=random.shuffle(valid_stores)
)

# upc: too long
item4 = model.Item(
    name=(''.join(random.choices(string.ascii_letters, k=32))),
    upc=(''.join(random.choices(string.digits, k=13))),
    stores=random.shuffle(valid_stores)
)

# stores: invalid store array
item5 = model.Item(
    name='Target',
    upc=(''.join(random.choices(string.digits, k=12))),
    stores=invalid_stores
)

invalid_items = [
    item2,
    item3,
    item4,
    item5
]