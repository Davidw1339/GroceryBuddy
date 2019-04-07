from flask import Blueprint, request
import model
import json
from utils import Error

search_blueprint = Blueprint("search", __name__)


@search_blueprint.route("/search", methods=['GET'])
def search():
    '''
        Body: {"keyword", "upc"]}
        Response:
            - {"success": true or false},
            - {"error": error description}
    '''
    upc = request.args.get('upc')
    keyword = request.args.get('keyword')
    if upc:
        return model.Item.objects(upc=upc).to_json()
    elif keyword:
        return model.Item.objects(name__icontains=keyword).to_json()
    else:
        return json.dumps({'success': False, 'error': Error.MISSING_KEYWORD_UPC.value})
