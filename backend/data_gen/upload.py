import requests
import json
import random


def load_data():
    '''
    Loads the data from a JSON file
    '''
    with open("insta_dump.json") as f:
        return json.load(f)


def upload_items(data):
    '''
    Uploads given item data to the database
    '''
    for i, obj in enumerate(data):
        r = requests.post(
            'https://grocerybuddybackend.azurewebsites.net/item', json=obj)
        print(i, r.text)


def upload_prices(data):
    '''
    Uploads given price data to the database
    '''
    for i, obj in enumerate(data):
        r = requests.post(
            'https://grocerybuddybackend.azurewebsites.net/price', json=obj)
        print(i, r.text)


def direct_upload():
    '''
    Uploads the data from JSON save as-is
    '''
    data = load_data()
    upload_items(data)


def add_stores(items, stores):
    '''
    Adds additional stores to the data.
    stores should be a list of dictionaries with the following fields:
        'store': Store name
        'lat': Latitude of store
        'long': Longitude of store
        'mult_floor': Lower bound on the random price multiplier
        'mult_ceil': Upper bound on the random price multiplier
    '''
    additional_prices = []
    for item in items:
        for store in stores:
            orig_price = item['price']
            multiplier = random.uniform(
                store['mult_floor'], store['mult_ceil'])
            new_price = round(multiplier * orig_price, 2)
            price_data = {
                'upc': item['upc'],
                'user': 'instacart',
                'store': store['store'],
                'lat': store['lat'],
                'long': store['long'],
                'price': new_price
            }
            additional_prices.append(price_data)
    return additional_prices


def multistore_upload(stores):
    '''
    Uploads the JSON data with additional stores.
    See add_stores for stores argument format.
    '''
    items = load_data()
    additional_prices = add_stores(items, stores)
    upload_items(items)
    upload_prices(additional_prices)


if __name__ == '__main__':
    stores = [
        {
            'store': 'Aldi',
            'lat': 40.149089,
            'long': -88.25785,
            'mult_floor': 0.6,
            'mult_ceil': 1.1
        },
        {
            'store': 'County Market',
            'lat': 40.113049,
            'long': -88.233976,
            'mult_floor': 0.8,
            'mult_ceil': 1.2
        },
        {
            'store': 'Harvest Market',
            'lat': 40.090844,
            'long': -88.248054,
            'mult_floor': 0.9,
            'mult_ceil': 1.4
        }
    ]
    multistore_upload(stores)
