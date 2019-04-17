import model
from datetime import datetime
import base64


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
    date=datetime(2019, 3, 10, 11, 30, 12).timestamp()
)

# valid
price1 = model.Price(
    user='admin',
    upvotes=users(7),
    downvotes=users(4, 7),
    price=0.99,
    date=datetime(2019, 3, 10, 11, 30, 42).timestamp()
)

# valid
price2 = model.Price(
    user='admin',
    upvotes=[],
    downvotes=[],
    price=0.00,
    date=datetime(2019, 3, 10, 11, 31, 22).timestamp()
)

# valid
price3 = model.Price(
    user='admin',
    upvotes=users(200),
    downvotes=users(1000, 200),
    price=139.99,
    date=datetime(2019, 3, 10, 11, 31, 52).timestamp()
)

# valid
price4 = model.Price(
    user='admin',
    upvotes=users(20),
    downvotes=users(19, 20),
    price=12.89,
    date=datetime(2019, 3, 10, 12, 30, 12).timestamp()
)

# valid
price9 = model.Price(
    user='testuser',
    upvotes=[],
    downvotes=[],
    price=4.95,
    date=datetime(2019, 3, 10, 12, 30, 32).timestamp()
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
    date=datetime(2019, 3, 9, 11, 30, 12).timestamp()
)

# price: negative price
price6 = model.Price(
    user='admin',
    upvotes=users(200),
    downvotes=users(1000, 200),
    price=-139.99,
    date=datetime(2019, 3, 8, 11, 30, 12).timestamp()
)

# none fields
price7 = model.Price(
    user=None,
    upvotes=None,
    downvotes=None,
    price=None,
    date=datetime(2019, 3, 7, 11, 30, 12).timestamp()
)

# price: too many digits in cents
price8 = model.Price(
    user='admin',
    upvotes=users(200),
    downvotes=users(100, 200),
    price=19.999,
    date=datetime(2019, 3, 6, 11, 29, 12).timestamp()
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
        'lat': 10,
        'long': 10
    },
    prices=valid_prices
)

# valid
store2 = model.Store(
    name='Target',
    location={
        'lat': .01,
        'long': .01
    },
    prices=valid_prices[::-1]
)

# valid
store3 = model.Store(
    name='Meijer',
    location={
        'lat': 30,
        'long': 30
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

store11 = model.Store(
    name='Safeway',
    location={
        'lat': 40.1516,
        'long': -88.2273
    },
    prices=[
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
    store11
]

# name: name too long
store4 = model.Store(
    name='mwRgzdmj1wZRELlZTlVMmpKhkvEQeR11ncoUae2I9gPAXPFpWqxsJT5AHTRvXEP1j',
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

# invalid lat type
store12 = model.Store(
    name='Walmart',
    location={
        'lat': 'hi',
        'long': 0
    },
    prices=[
        price0,
    ]
)

# invalid long type
store13 = model.Store(
    name='Target',
    location={
        'lat': 0,
        'long': 'hi'
    },
    prices=[
        price0,
    ]
)

# missing lat
store14 = model.Store(
    name='Walmart',
    location={
        'long': 0
    },
    prices=[
        price0,
    ]
)

# missing long
store15 = model.Store(
    name='Target',
    location={
        'lat': 0
    },
    prices=[
        price0,
    ]
)

invalid_stores = [
    store4,
    store5,
    store6,
    store7,
    store8,
    store9,
    store12,
    store13,
    store14,
    store15
]

item0 = model.Item(
    name='apple',
    upc='042100005264',
    stores=valid_stores
)

item1 = model.Item(
    name='milk',
    upc='787735087189',
    stores=valid_stores[::-1]
)

item6 = model.Item(
    name='testItem1',
    upc='042100005265',
    stores=valid_stores[0:3]
)

item7 = model.Item(
    name='testItem2',
    upc='042100005266',
    stores=valid_stores[1:3]
)

item8 = model.Item(
    name='Candy',
    upc='770128241494',
    stores=valid_stores[0:1],
    image_url='http://www.sweetcitycandy.com/blog/wp-content/uploads/2015/06/Skittles-1024x1003.jpg'
)

# Valid item with image.
# Encode image field if testing add_item (because add_item decodes it).
item13 = model.Item(
    name='Mouse',
    upc='725128241494',
    stores=valid_stores[0:1],
    image=base64.b64decode('/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////2wBDAf//////////////////////////////////////////////////////////////////////////////////////wAARCAGQASwDASIAAhEBAxEB/8QAFwABAQEBAAAAAAAAAAAAAAAAAAECA//EACQQAQEBAAEEAwABBQAAAAAAAAABEQIhMUFREnGBkSJhscHw/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAH/xAAVEQEBAAAAAAAAAAAAAAAAAAAAEf/aAAwDAQACEQMRAD8AAAAAKgCgArN738aZve/gI1OzLUAAA4+ftU4+ftQQKAAAAAAAAAAAAAAAAAKigIAIAAAAACgArN736/20ze/4CLEWAoAHHvVSd7+NAzQoAAAAAAAAAAAAAAAAAqKCKigyAAAAACiKCpy8fx/KlmwGFT/KgqBvrrQXj5aSTIoJUVAAAAAAAAAAAAAAAAAAAFRQZAAAAAAVAGoqRQSyVPjGgGfjFyRQAAERWQUQBQAAAAAAAAAAAAAAAAAQAAAAAAAGoqRQAAAAAARlpKCAAoigAAAAAgKAAIAoAAAAAIAAAAAAADUVIoAAAAAIAlVAQABUAUTf7GgoAIKAgAAAKAAAAACCgIKAgoCAoLFQBQQFEigItQBFQEAAUEAkwAABQARBQEAUUAARQGb3aAAAAAAABDQaAAUAAAEVAEVARYigAIAAACKAKgACAKKACKigIqAompoKayA1qagAADaueroNjKgqooCKgCKgAAAMy6g0AAAigCoAAgJqjQmgCooDFvVtzoKIoIoAAAAAAbgNQYXr7Btpz2+12+wbRnr7qf8AdwaTYyAu9WmGpQVMm6oAkvXMDQVAQZtanbqAAAFQFAAAAC3ow1WQa6UysgNCbfZt9guURAa6G+oyAuouAEVGgFQBUXwgAAIADUujC6DSJqoqiaqoCJoNM6mgKqKAAAADNRagLUVAAAWFIUEa6MgKgANstQFEAa1k2GoACiAAiKAGoApqAAACooKqKAAACAlRUBUUBAABQEFARQAVFBSpqaAAAABqoAAAAAigAAACgKigAAIqAiKgNI13ZAAAVFBBUAAAAAAAAAAAAAAAAAAAFAAAUAAEABAEUAavtlqegZFqAAAAuAgKCGKoMjSYCBgAAAAAAAAAAAqAKGgKIAAAIqAAACAN3LGQAXUFKtQAAEF0QBRFAABBQEAAAAAAAAAAABdEAUNAEVAAARQAAUAAAAAEAAAAAAAAAFBAAAAAAAAAAAAAAUQAABBcMoAvxq/EGRr4nxoMhlAAAAAAAAAAXKC8e7qzOM/Wgc+Uxh15dnIAAAAAAAAAAAAAAAAHUAAY5b+Mg6jlq7QdGbxJynno0DkOlmuYAAAAAAOnGeW3PjfDoAACXrHGu7HKeQcwARUAUAAAAAAAAAAAHTdVzlxr5QGmLx9NaA5jfyif00GVlz6LMQHXuzynlnjcdAchb0qAAAAALqAK1OVnfqwA7y6OMtjV5gxQAQVAFRQAAAAAAAAAAQUBF2iAKgDUthZvWMrLgDfGpm9YslgHKMOrnegICggAAAAAAAAACKAi+EWefoAAAAAAAAAAAAAAEAAABZcdHJrjQdGeU8tAOSl6IAAAAAAAAAAAACNce/4i8e9+gQAAAAAAAAAAAAAEAAAAAB043WnKXHTuCcp5YdGLMoIAAAAAAAAAAAA1OktZavSYDIAAAAAAAAAAAAACKAgAAADXG+GQHZLNSXWgchrlPLIAAAAAAAAALJoLxnlm3a1bnRgFAAAAAAAAAAAAAAAARUAAAABZcro5LLgOjNnlqXQHMas9MgAAAAA1OPsEk1q2SFsjHcARQAAAAAAAAAAf/9k='))

valid_items = [
    item0,
    item1,
    item6,
    item7,
    item8
]

# name: too many characters
item2 = model.Item(
    name='AcQzhluGIisirQPlAkHrhhTTQttPCtIYCFaVHWuNDVzaPnuXdYQkmkkmUBkJGJfhw',
    upc='592227616260',
    stores=valid_stores[-1:] + valid_stores[:-1]
)

# upc: too short
item3 = model.Item(
    name='hLeLIyWqJtIzirgHSJGwSTGBzHzFIpyo',
    upc='9093280452',
    stores=valid_stores
)

# upc: too long
item4 = model.Item(
    name='xUIgqVRdgGjahkzGonOQGEblMhUYZKXy',
    upc='8427676361505',
    stores=valid_stores[::-1]
)

# stores: invalid store array
item5 = model.Item(
    name='Target',
    upc='881132924739',
    stores=invalid_stores
)

# stores: store with invalid lat
item9 = model.Item(
    name='Food',
    upc='881132924239',
    stores=[store12]
)

# stores: store with invalid long
item10 = model.Item(
    name='Milk',
    upc='881135924239',
    stores=[store13]
)

# stores: store with missing lat
item11 = model.Item(
    name='Eggs',
    upc='881132924209',
    stores=[store14]
)

# stores: store with missing long
item12 = model.Item(
    name='Toy',
    upc='881135924739',
    stores=[store15]
)

invalid_items = [
    item2,
    item3,
    item4,
    item5,
    item9,
    item10,
    item11,
    item12
]
