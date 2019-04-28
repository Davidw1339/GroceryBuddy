import json
import search
import test_data
import copy
from utils import Error
from math import sin, cos, sqrt, atan2, radians


def test_search_close(client, db):
    '''
    Tests searching for the closest stores
    within 10 miles.
    '''
    for i in test_data.valid_items:
        copy.deepcopy(i).save()

    lat = 0
    long = 0
    miles = 10

    rv = client.get('/search_gps?lat=' + str(lat) + "&long=" +
                    str(long) + "&miles=" + str(miles))
    response = json.loads(rv.data)

    stores_in_range = compute_stores_in_range(
        test_data.valid_items, lat, long, miles)

    assert len(response) == len(stores_in_range)


def test_search_1000(client, db):
    '''
    Tests searching for the closest stores
    within 1000 miles.
    '''
    for i in test_data.valid_items:
        copy.deepcopy(i).save()

    lat = 0
    long = 0
    miles = 1000

    rv = client.get('/search_gps?lat=' + str(lat) + "&long=" +
                    str(long) + "&miles=" + str(miles))
    response = json.loads(rv.data)

    stores_in_range = compute_stores_in_range(
        test_data.valid_items, lat, long, miles)

    assert len(response) == len(stores_in_range)


def compute_stores_in_range(items, lat, lon, miles):
    '''
    A verifier that independently computes how
    many stores are in range of a location.
    '''
    seen = set()
    list_of_stores = []
    for item in items:
        for store in item.stores:
            store_lat = store['location']['lat']
            store_long = store['location']['long']
            store_entry = {
                'name': store['name'],
                'lat': store_lat,
                'long': store_long
            }
            t = tuple(store_entry.items())
            if t not in seen:
                seen.add(t)
                list_of_stores.append(store_entry)

    list_of_stores_gps = []
    for store in list_of_stores:
        earth_radius = 3963.0

        lat1 = radians(lat)
        lon1 = radians(lon)
        lat2 = radians(store['lat'])
        lon2 = radians(store['long'])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = earth_radius * c
        if distance <= float(miles):
            list_of_stores_gps.append(store)
    return list_of_stores_gps
