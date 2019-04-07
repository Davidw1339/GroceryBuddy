from flask import Blueprint, request
import json
import validation
from utils import Error
import mongoengine.errors
import model

optimal_store_blueprint = Blueprint("optimal_store", __name__)


@optimal_store_blueprint.route('/optimal_store', methods=['POST'])
def get_optimal_store():
    """
        Body: {"single_store": boolean, single or multiple stores, "items": [upc:String]}
        Response:   {"success": True or False,
                    "error": error description,
                    "optimal_prices":
                            [{"store": store,
                              "upcs": list of upcs,
                              "price": total price of items associated with store}]
                    }
    """
    error = Error.NO_ERROR.value
    data = request.get_json(force=True)
    if data is None:
        error = Error.INVALID_JSON.value
        return json.dumps({'success': False, 'error': error, 'optimal_prices': None})

    item_list = []
    items = data['items']
    if items is None:
        error = Error.MISSING_UPC.value
        return json.dumps({'success': False, 'error': error, 'optimal_prices': None})
    for upc in items:
        result = model.Item.objects(upc=upc)
        if len(result) == 0:
            error = Error.UPC_DNE.value
        else:
            item_list.append(result.to_json())

    upc_dict = {}
    for item in item_list:
        item = json.loads(item)
        upc = item[0]['upc']
        for store in item[0]['stores']:
            store_key = str(store['name']) + '|' + str(store['location']
                                                       ['lat']) + '|' + str(store['location']['long'])
            latest_price = store['prices'][-1]['price']
            upc_list = upc_dict.get(upc)
            if upc_list is None:
                upc_dict[upc] = [(store_key, latest_price)]
            else:
                upc_list.append((store_key, latest_price))

    single_store = data['single_store']
    if single_store:
        store_dict_price = {}  # key: store, value: list of prices
        store_dict_upc = {}
        for upc, store_price_list in upc_dict.items():
            for store_price in store_price_list:
                store = store_dict_price.get(store_price[0])
                if store is None:
                    store_dict_price[store_price[0]] = [store_price[1]]
                    store_dict_upc[store_price[0]] = [upc]
                else:
                    store.append(store_price[1])
                    store_dict_upc[store_price[0]].append(upc)
        lowest_price = None  # tuple (store unique str, total_price)
        item_count = 0
        for store, price_list in store_dict_price.items():
            total_price = sum(price_list)
            bigger = len(price_list) > item_count
            equal_and_cheaper = len(
                price_list) == item_count and total_price < lowest_price[1]
            if lowest_price is None or bigger or equal_and_cheaper:
                lowest_price = (store, total_price)
                item_count = len(price_list)

        store_info = lowest_price[0].split('|')
        store_obj = {
            'name': store_info[0],
            'location': {
                'lat': store_info[1],
                'long': store_info[2]
            },
            'prices': []
        }
        return json.dumps({'success': True, 'error': error, 'optimal_prices':
                                            [{"store": store_obj,
                                                "upcs": store_dict_upc[lowest_price[0]],
                                                "price": lowest_price[1]}]
                           })
    else:
        store_dict = {}  # key: store, value: list of tuples (upc, price)
        for upc, store_price_list in upc_dict.items():
            best_store_price = None
            for store_price in store_price_list:
                if best_store_price is None or store_price[1] < best_store_price[1]:
                    best_store_price = store_price
            store_dict_entry = store_dict.get(best_store_price[0])
            if store_dict_entry is None:
                store_dict[best_store_price[0]] = [(upc, best_store_price[1])]
            else:
                store_dict[best_store_price[0]].append(
                    (upc, best_store_price[1]))
        optimal_prices = []
        for store, upc_price_list in store_dict.items():
            store_info = store.split('|')
            store_obj = {
                'name': store_info[0],
                'location': {
                    'lat': store_info[1],
                    'long': store_info[2]
                },
                'prices': []
            }
            upcs = []
            total_price = 0
            for upc_price in upc_price_list:
                upcs.append(upc_price[0])
                total_price += upc_price[1]
            optimal_prices.append(
                {'store': store_obj, 'upcs': upcs, 'price': total_price})
        return json.dumps({'success': True, 'error': error, 'optimal_prices': optimal_prices})
