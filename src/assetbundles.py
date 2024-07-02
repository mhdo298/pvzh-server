from flask import Blueprint, redirect
from utils import r

assetbundles = Blueprint('assetbundles', __name__, url_prefix='/assetbundles')


@assetbundles.route('/<path:path>', methods=['GET'])
def bundles(path):
    if path.endswith('/manifest_version'):
        version = r.incr('version', 1)
    return redirect('https://pvzheroes-live.ecs.popcap.com/assetbundles/' + path)
