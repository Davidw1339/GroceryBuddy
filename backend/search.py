from flask import Blueprint, request
import model
import json
from utils import Error

search_blueprint = Blueprint("search", __name__)


@search_blueprint.route("/search", methods=['GET'])
def search():
    '''
        Body: {one of ["keyword", "upc"], ["limit"]}
        Response:
            - {"success": true or false},
            - {"error": error description}

    Returns all items containing the given keyword or
    with the given UPC. If limit is given, returns at most
    that number of items.
    '''
    upc = request.args.get('upc')
    keyword = request.args.get('keyword')
    limit_arg = request.args.get('limit')
    if limit_arg:
        if limit_arg.isdigit() and int(limit_arg) > 0:
            limit = int(limit_arg)
        else:
            return json.dumps({'success': False, 'error': Error.INVALID_LIMIT.value})
    else:
        limit = None

    if upc:
        results = model.Item.objects(upc=upc)
    elif keyword:
        results = model.Item.objects(name__icontains=keyword)
    else:
        return json.dumps({'success': False, 'error': Error.MISSING_KEYWORD_UPC.value})

    results = results.order_by('+upc')

    if limit:
        results = results[:limit]

    results_json = results.exclude('image').to_json()
    return results_json
