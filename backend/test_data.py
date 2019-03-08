import model
import random
import string
from datetime import datetime


def users(num, start=0):
    '''
    Generates a list of usernames for upvote/downvote lists
    '''
    return ['user' + str(i) for i in range(start, start+num)]


# valid
price0 = model.Price(
    user='admin',
    upvotes=users(10),
    downvotes=users(5, 10),
    price=1.99,
    date=datetime.now().timestamp()
)

# valid
price1 = model.Price(
    user='admin',
    upvotes=users(7),
    downvotes=users(4, 7),
    price=0.99,
    date=datetime.now().timestamp()
)

# valid
price2 = model.Price(
    user='admin',
    upvotes=[],
    downvotes=[],
    price=0.00,
    date=datetime.now().timestamp()
)

# valid
price3 = model.Price(
    user='admin',
    upvotes=users(200),
    downvotes=users(1000, 200),
    price=139.99,
    date=datetime.now().timestamp()
)

# valid
price4 = model.Price(
    user='admin',
    upvotes=users(20),
    downvotes=users(19, 20),
    price=12.89,
    date=datetime.now().timestamp()
)

# valid
price9 = model.Price(
    user='testuser',
    upvotes=[],
    downvotes=[],
    price=4.95,
    date=datetime.now().timestamp()
)

# array of valid prices
valid_prices = [
    price0,
    price1,
    price2,
    price3,
    price4,
    price9,
]

# user: empty string
price5 = model.Price(
    user='',
    upvotes=users(10),
    downvotes=users(5, 10),
    price=1.99,
    date=datetime.now().timestamp()
)

# price: negative price
price6 = model.Price(
    user='admin',
    upvotes=users(200),
    downvotes=users(1000, 200),
    price=-139.99,
    date=datetime.now().timestamp()
)

# none fields
price7 = model.Price(
    user=None,
    upvotes=None,
    downvotes=None,
    price=None,
    date=datetime.now().timestamp()
)

# price: too many digits in cents
price8 = model.Price(
    user='admin',
    upvotes=users(200),
    downvotes=users(100, 200),
    price=19.999,
    date=datetime.now().timestamp()
)

# array of invalid prices
invalid_prices = [
    price5,
    price6,
    price7,
    price8,
]

# valid
store0 = model.Store(
    name='Walmart',
    location={
        'lat': 0,
        'long': 0
    },
    prices=[price0, price1]
)

# valid
store1 = model.Store(
    name='County Market',
    location={
        'lat': 0,
        'long': 0
    },
    prices=valid_prices
)

# valid
store2 = model.Store(
    name='Target',
    location={
        'lat': 0,
        'long': 0
    },
    prices=random.sample(valid_prices, k=len(valid_prices))
)

# valid
store3 = model.Store(
    name='Meijer',
    location={
        'lat': 0,
        'long': 0
    },
    prices=[
        price0,
        price2,
        price1,
    ]
)

# valid, not added to array
store10 = model.Store(
    name='Whole Foods',
    location={
        'lat': 0,
        'long': 0
    },
    prices=[
        price0,
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
    prices=[
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
    prices=[
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
    prices=[
        price2,
        price0,
    ]
)

# location: extra field
store7 = model.Store(
    name='Walmart',
    location={
        'lat': 0,
        'long': 0,
        'rand': None
    },
    prices=[
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
    prices=invalid_prices
)

# empty fields
store9 = model.Store(
    name=None,
    location=None,
    prices=None
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
    stores=random.sample(valid_stores, k=len(valid_stores))
)

valid_items = [
    item0,
    item1,
]

# name: too many characters
item2 = model.Item(
    name=(''.join(random.choices(string.ascii_letters, k=65))),
    upc=(''.join(random.choices(string.digits, k=12))),
    stores=random.sample(valid_stores, k=len(valid_stores))
)

# upc: too short
item3 = model.Item(
    name=(''.join(random.choices(string.ascii_letters, k=32))),
    upc=(''.join(random.choices(string.digits, k=10))),
    stores=random.sample(valid_stores, k=len(valid_stores))
)

# upc: too long
item4 = model.Item(
    name=(''.join(random.choices(string.ascii_letters, k=32))),
    upc=(''.join(random.choices(string.digits, k=13))),
    stores=random.sample(valid_stores, k=len(valid_stores))
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
