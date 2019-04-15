from flask import Blueprint, request, send_file
import io
from utils import Error
import validation
import json
import model

get_image_blueprint = Blueprint("get_image", __name__)


@get_image_blueprint.route('/get_image', methods=['GET'])
def get_image():
    '''
    Body: {"upc"}
    Response: image/jpeg if successful
    Otherwise,
        {"success": false,
         "error": error description}

    This route serves the JPEG image saved for the item with the given UPC.
    The HTTP response resembles the response for a direct link to a JPEG file
    (as if the frontend had made a GET request to example.com/photo.jpg).
    '''
    upc = request.args.get('upc')
    if not upc:
        return json.dumps({'success': False, 'error': Error.MISSING_FIELDS.value})

    item = model.Item.objects(upc=upc).first()
    if item is None:
        return json.dumps({'success': False, 'error': Error.ITEM_DNE.value})

    if item.image is None:
        return json.dumps({'success': False, 'error': Error.NO_IMAGE.value})

    image_stream = io.BytesIO(item.image)

    return send_file(image_stream, mimetype='image/jpeg')
