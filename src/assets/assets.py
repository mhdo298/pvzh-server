import os
from asyncio import gather

base_url = os.getenv('ASSETS_URL')
initial_value = 20000

from quart import Blueprint, redirect, request

from src.utils.http import init_http, get_json
from src.utils.cache import init_redis
import orjson as json

assets = Blueprint('assets', __name__, url_prefix='/<string:username>/<string:repo>/assetbundles')


def register_assets(app):
    app.register_blueprint(assets)
    init_http(app)
    init_redis(app)


@assets.route("/ClientServerContentAssociations.txt")
async def client_server(username, repo):
    return redirect(f'https://{username}.github.io/{repo}/ClientServerContentAssociations.txt')


@assets.route("/<platform>/<version>/manifest_version")
async def update_manifest_version(username, repo, platform, version):
    version = initial_value + await request.redis.incr(f'{username}_{repo}_manifest_version')
    return str(version)


@assets.route("/<platform>/<version>/AssetPathsManifest")
async def asset_paths_manifest(username, repo, platform, version):
    content, version_cache, manifest_version = await gather(
        get_json(f'https://{username}.github.io/{repo}/AssetPathsManifest', '/asset_files/AssetPathsManifest'),
        get_json(f'https://{username}.github.io/{repo}/version.json', f'/{username}+{repo}/asset_files/version.json'),
        request.redis.get(f'{username}_{repo}_manifest_version')
    )
    for file in version_cache:
        content['BundleNameToDetails'][file]["Size"] = version_cache[file]["Size"]
        content['BundleNameToDetails'][file]["Version"] = initial_value + int(manifest_version) if version_cache[file]["Live"] else version_cache[file]["Version"]
    return json.dumps(content)


@assets.route("/<platform>/<version>/<path:request_file>")
async def get_assets(username, repo, platform, version, request_file):
    version_cache = await get_json(f'https://{username}.github.io/{repo}/version.json',
                                   f'/{username}+{repo}/asset_files/version.json')
    if request_file in version_cache:
        return redirect(f'https://{username}.github.io/{repo}/files/{version_cache[request_file]["Path"]}')
    else:
        return redirect(f'{base_url}/{platform}/{version}/{request_file}')
