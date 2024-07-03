import gzip

from flask import Blueprint, redirect, request, make_response
from utils import r, assets
from gzip import compress

assetbundles = Blueprint('assetbundles', __name__, url_prefix='/assetbundles')
mod_files = ['/cards/card_data', '/data_assets', '/fonts/inline_text_tag', '/loc/en']


@assetbundles.route('/<path:path>', methods=['GET'])
def bundles(path: str):
    for mod_file in mod_files:
        if mod_file in path:
            return redirect('https://storage.googleapis.com/devh-mod-files/files/' + path)
    if path.endswith('/manifest_version'):
        version = r.incr('manifest')
        return str(version)
    if path.endswith('/AssetPathsManifest'):
        version = r.get('manifest')
        content = gzip.compress(assets
                                .replace(b'"CARD_DATA_VERSION"', version)
                                .replace(b'"DATA_ASSETS_VERSION"', version)
                                .replace(b'"INLINE_TEXT_TAG_VERSION"', version)
                                .replace(b'"EN_VERSION"', version)
                                )
        response = make_response(content)
        response.headers['Content-length'] = len(content)
        response.headers['Content-Encoding'] = 'gzip'
        return response
    if 'if-none-match' in request.headers.keys():
        return (None, 304)
    return redirect('https://pvzheroes-live.ecs.popcap.com/assetbundles/' + path)
