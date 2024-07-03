import gzip

from flask import Blueprint, redirect, request, make_response
from utils import r, assets
from gzip import compress

assetbundles = Blueprint('assetbundles', __name__, url_prefix='/assetbundles')


@assetbundles.route('/<path:path>', methods=['GET'])
def bundles(path: str):
    if path.endswith('/cards/card_data'):
        return redirect('https://github.com/PrplGreen2/Syndrome/releases/download/v4.1.0.2.2/card_data_173')
    if path.endswith('/data_assets'):
        return redirect('https://github.com/PrplGreen2/Syndrome/releases/download/v4.1.0.2.2/data_assets_360')
    if path.endswith('/fonts/inline_text_tag'):
        return redirect('https://github.com/PrplGreen2/Syndrome/releases/download/v4.1.0.2.2/inline_text_tag_40')
    if path.endswith('/loc/en'):
        return redirect('https://github.com/PrplGreen2/Syndrome/releases/download/v4.1.0.2.2/en_296')

    if path.endswith('/manifest_version'):
        version = r.incr('manifest')
        return version
    if path.endswith('/AssetPathsManifest'):
        version = r.get('manifest')
        content = (assets
                   .replace(b'"CARD_DATA_VERSION"', version)
                   .replace(b'"DATA_ASSETS_VERSION"', version)
                   .replace(b'"INLINE_TEXT_TAG_VERSION"', version)
                   .replace(b'"EN_VERSION"', version)
                   )
        return content
    if 'if-none-match' in request.headers.keys():
        return (None, 304)
    # if path.endswith('/manifest.json'):
    return redirect('https://pvzheroes-live.ecs.popcap.com/assetbundles/' + path)
