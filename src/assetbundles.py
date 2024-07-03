from flask import Blueprint, redirect, request
from utils import r

assetbundles = Blueprint('assetbundles', __name__, url_prefix='/assetbundles')


@assetbundles.route('/<path:path>', methods=['GET'])
def bundles(path):
    if 'if-none-match' in request.headers.keys():
        print(request.headers.get_all('if-none-match'))
        return (None, 304)
    # if path.endswith('/manifest_version'):
    #     version = r.incr('manifest')
    #     return str(version)
    # if path.endswith('/manifest.json'):
    return redirect('https://pvzheroes-live.ecs.popcap.com/assetbundles/' + path)
