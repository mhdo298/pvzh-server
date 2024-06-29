from flask import Blueprint, request

from utils import get_id, it_should_be_there_soon, make_entity_model, make_rng

pvp = Blueprint('pvp', __name__, url_prefix='/pvp/v1')


@pvp.route('/initGame')
def init_game():
    pid = get_id()
    data = request.get_json()
    gi = data['gi']
    seed1 = it_should_be_there_soon(pid + '-seed')
    seed2 = it_should_be_there_soon(gi + '-seed')
    seed = seed1 ^ seed2
    sd1 = it_should_be_there_soon(pid + '-sd')
    sd2 = it_should_be_there_soon(gi + '-sd')

    return {
        "entityModel": make_entity_model(sd1, sd2),
        "rngSeedData": make_rng(seed),
        "ec": "CgQgACgA",
        "sc": "",
        "tec": "",
        "cec": "EAE=",
        "ty": "InitialGameState",
        "plays": "{}",
        "gst": "0"
    }


@pvp.route('/pvpSendUpdate')
def pvp_send_update():
    return {}


@pvp.route('/pvpPoll')
def pvp_poll():
    pass


@pvp.route('/history')
def make_match():
    return {
        "seasons": {},
        "version": None,
        "id": get_id()
    }


@pvp.route('/playerPvpData')
def player_pvp_data():
    return {
        "gamesPlayed": 0,
        "stars": 0,
        "id": get_id(),
        "version": None,
        "season": "season_73",
        "wins": 0,
        "losses": 0,
        "mmr": 1600,
        "rank": 50,
        "streakBonus": 0,
        "wonLastGame": False
    }
