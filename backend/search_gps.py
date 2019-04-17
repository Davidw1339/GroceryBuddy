from flask import Blueprint, request
import model
import json
from utils import Error
from math import sin, cos, sqrt, atan2, radians


search_gps_blueprint = Blueprint("search_gps", __name__)


@search_gps_blueprint.route("/search_gps", methods=['GET'])
def search_gps():
    '''
        Query Params: lat-latitude, long-longitude, miles-radius in miles
        Response:
            [{
                "name": name of store,
                "lat": latitude of store,
                "long": longitude of store
                "distance": distance of store from given point
            }]

    Returns all stores within given radius of given lat,long sorted by distance
    '''

    lat = float(request.args.get('lat', default=0))
    lon = float(request.args.get('long', default=0))
    miles = request.args.get('miles', default=10)

    items = model.Item.objects().only('stores')

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
            store["distance"] = distance
            list_of_stores_gps.append(store)
    list_of_stores_gps = sorted(list_of_stores_gps, key=lambda i: i['distance'])

    return json.dumps(list_of_stores_gps)
