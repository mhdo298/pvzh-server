from asyncio import gather

import orjson as json

from quart import Blueprint

from src.persistence.get_data import get_user_data, get_decks_data
from src.utils.database import init_db
from src.utils.http import get_json, init_http
from src.utils.misc import get_id, merge_json

persistence = Blueprint('persistence', __name__, url_prefix='/<string:username>/<string:repo>/persistence')


def register_persistence(app):
    app.register_blueprint(persistence)
    init_http(app)
    init_db(app)


@persistence.route('/<version>/ping')
async def ping(username, repo, version):
    return 'ping'


@persistence.route('/<version>/user/sync', methods=['POST'])
async def user(username, repo, version):
    mod_name = f'{username}+{repo}'
    user_config, existing_data = await gather(
        get_json(f'https://{username}.github.io/{repo}/configs/user.json',
                 f'/{mod_name}/configs/user.json'),
        get_user_data(mod_name))
    merge_json(user_config, existing_data)
    return json.dumps(user_config)


@persistence.route('/<version>/inventory/sync', methods=['POST'])
async def inventory(username, repo, version):
    mod_name = f'{username}+{repo}'
    inventory_config, existing_data = await gather(
        get_json(f'https://{username}.github.io/{repo}/configs/inventory.json',
                 f'/{mod_name}/configs/inventory.json'),
        get_user_data(mod_name))
    merge_json(inventory_config, existing_data)
    inventory_config["Id"] = get_id()
    return json.dumps(inventory_config)


@persistence.route('/<version>/decks/sync', methods=['POST'])
async def decks(username, repo, version):
    mod_name = f'{username}+{repo}'
    all_decks = await get_decks_data(mod_name)
    return {
        "version": 1,
        "Id": get_id(),
        "Decks": all_decks
    }


@persistence.route('/<version>/playerInfo', methods=['GET'])
async def player_info(username, repo, version):
    mod_name = f'{username}+{repo}'
    player_info_config = await get_json(f'https://{username}.github.io/{repo}/configs/playerInfo.json',
                                        f'/{mod_name}/configs/playerInfo.json')
    player_info_config["Id"] = get_id()
    return json.dumps(player_info_config)
