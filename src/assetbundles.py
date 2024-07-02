from flask import Blueprint, redirect

assetbundles = Blueprint('assetbundles', __name__, url_prefix='/assetbundles')


@assetbundles.route('/<path:path>', methods=['GET'])
def ftue_bundles(path):
    return redirect('https://pvzheroes-live.ecs.popcap.com/assetbundles/' + path)
