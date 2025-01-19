from asyncio import gather, timeout
from random import getrandbits

import orjson as json

from quart import Blueprint, request

from src.utils.cache import init_redis
from src.utils.misc import get_id

matchmaking = Blueprint('matchmaking', __name__, url_prefix='/<string:username>/<string:repo>/matchmaking')


def register_matchmaking(app):
    app.register_blueprint(matchmaking)
    init_redis(app)


@matchmaking.route('/<version>/queryStats', methods=['POST'])
async def query_stats(username, repo, version):
    return {
        "fastestRankedMatch": "None",
        "fastestCasualMatch": "None"
    }


@matchmaking.route('/<version>/createChallenge', methods=['POST'])
async def create_challenge(username, repo, version):
    data = await request.get_json()
    mod_name = f'{username}+{repo}'
    player_data = json.loads(data['sd'])
    challenger = player_data['PlayerId']
    challenged = data['o']
    seed_contribution = getrandbits(60)
    await request.redis.rpush(f'{mod_name}-{challenger}-matchinfo', data['sd'], seed_contribution)
    await request.redis.expire(f'{mod_name}-{challenger}-matchinfo', 20)
    return {
        "ty": "JoinMatch",
        "eta": 0,
        "gi": challenged
    }


@matchmaking.route('/<version>/makeMatch', methods=['POST'])
async def make_match(username, repo, version):
    data = await request.get_json()
    mod_name = f'{username}+{repo}'
    queue_type = data['q']
    faction = data['f']
    player_data = json.loads(data['sd'])
    challenger = player_data['PlayerId']
    await request.redis.rpush(f'{mod_name}-{queue_type}-{faction}', challenger)
    return {
        "ty": "WaitingForMatch",
        "eta": 30,
        "gi": None
    }


@matchmaking.route('/<version>/matchPoll', methods=['POST'])
async def match_poll(username, repo, version):
    data = await request.get_json()
    mod_name = f'{username}+{repo}'
    queue_type = data['q']
    faction = data['f']
    player_data = json.loads(data['sd'])
    opposite = 'P' if faction == 'Z' else 'Z'
    challenger = player_data['PlayerId']
    opponent = await request.redis.fcall('VPOP', 2,
                                         f'{mod_name}-{queue_type}-{opposite}',
                                         f'{mod_name}-{queue_type}-{faction}',
                                         challenger)
    if opponent is not None:
        await request.redis.rpush(f'{mod_name}-{queue_type}-{opposite}-{opponent.decode()}', challenger)
        await request.redis.expire(f'{mod_name}-{queue_type}-{opposite}-{opponent.decode()}', 20)
    else:
        opponent = await request.redis.blpop([f'{mod_name}-{queue_type}-{faction}-{challenger}'], 5)
        if opponent is None:
            return {
                "ty": "RepollForMatch",
                "eta": 0,
                "gi": None
            }
        opponent = opponent[1]
    seed_contribution = getrandbits(60)
    await request.redis.rpush(f'{mod_name}-{challenger}-matchinfo', data['sd'], seed_contribution)
    await request.redis.expire(f'{mod_name}-{challenger}-matchinfo', 20)
    return {
        "ty": "JoinMatch",
        "eta": 0,
        "gi": opponent.decode()
    }


@matchmaking.route('/<version>/joinMatch', methods=['POST'])
async def join_match(username, repo, version):
    data = await request.get_json()
    mod_name = f'{username}+{repo}'
    gi = data['gi']
    sd = await request.redis.blmove(f'{mod_name}-{gi}-matchinfo', f'{mod_name}-{gi}-matchinfo', 5)
    return {
        "ty": "MatchReady",
        "sd": sd.decode(),
        "gi": gi,
        "or": 1
    }


@matchmaking.route('/<version>/cancelMatch', methods=['POST'])
async def cancel_match(username, repo, version):
    pid = get_id()
    mod_name = f'{username}+{repo}'
    async with request.redis.pipeline(transaction=True) as pipe:
        await (pipe.lrem(f'{mod_name}-casual-Z', 0, pid)
               .lrem(f'{mod_name}-casual-P', 0, pid)
               .lrem(f'{mod_name}-ranked-Z', 0, pid)
               .lrem(f'{mod_name}-ranked-P', 0, pid)
               .execute()
               )
    return {
        "ty": "MatchCancelled"
    }
