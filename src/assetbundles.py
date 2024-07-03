import gzip

from flask import Blueprint, redirect, request, make_response
from utils import r, assets
from gzip import compress

assetbundles = Blueprint('assetbundles', __name__, url_prefix='/assetbundles')


@assetbundles.route('/<path:path>', methods=['GET'])
def bundles(path: str):
    if path.endswith('/manifest_version'):
        version = r.incr('manifest')
        return str(version)
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
