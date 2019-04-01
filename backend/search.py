from flask import Blueprint, request
from enum import Enum
import model
import json

search_blueprint = Blueprint("search", __name__)

class Error(Enum):
    MISSING_KEYWORD_UPC = 'Request does not contain keyword or upc code'

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