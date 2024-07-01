import json

from flask import Blueprint, request
from utils import r, it_should_be_there_soon, get_id
from random import getrandbits

matchmaking = Blueprint('matchmaking', __name__, url_prefix='/matchmaking/v1')


@matchmaking.route('/queryStats', methods=['GET'])
def query_stats():
    return {
        "fastestRankedMatch": "None",
        "fastestCasualMatch": "None"
    }


@matchmaking.route('/createChallenge', methods=['POST'])
def create_challenge():
    data = request.get_json()
    player_data = json.loads(data['sd'])
    challenger = player_data['PlayerId']
    challenged = data['o']
    seed_contribution = getrandbits(60)
    r.setex(challenger + "-sd", 20, data['sd'])
    r.setex(challenger + "-seed", 20, seed_contribution)
    return {
        "ty": "JoinMatch",
        "eta": 0,
        "gi": challenged
    }


@matchmaking.route('/joinMatch', methods=['POST'])
def join_match():
    data = request.get_json()
    gi = data['gi']
    return {
        "ty": "MatchReady",
        "sd": it_should_be_there_soon(gi + "-sd").decode(),
        "gi": gi,
        "or": 50
    }


@matchmaking.route('/makeMatch', methods=['POST'])
def make_match():
    data = request.get_json()
    faction = data['f']
    queue_type = data['q']
    player_data = json.loads(data['sd'])
    challenger = player_data['PlayerId']
    opposite = 'P' if faction == 'Z' else 'Z'
    challenged = r.lpop(queue_type + opposite)
    if challenged is not None:
        r.rpush(queue_type + challenger + faction, challenged.decode())
        r.rpush(queue_type + challenged.decode() + opposite, challenger)
    else:
        r.rpush(queue_type + faction, challenger)
    return {
        "ty": "WaitingForMatch",
        "eta": 30,
        "gi": None
    }


@matchmaking.route('/matchPoll', methods=['POST'])
def match_poll():
    data = request.get_json()
    faction = data['f']
    queue_type = data['q']
    player_data = json.loads(data['sd'])
    challenger = player_data['PlayerId']
    challenged = r.blpop([queue_type + challenger + faction], 4)
    if challenged is not None:
        seed_contribution = getrandbits(60)
        r.setex(challenger + "-sd", 20, data['sd'])
        r.setex(challenger + "-seed", 20, seed_contribution)
        return {
            "ty": "JoinMatch",
            "eta": 0,
            "gi": challenged[1].decode()
        }
    else:
        return {
            "ty": "RepollForMatch",
            "eta": 0,
            "gi": None
        }


@matchmaking.route('/cancelMatch', methods=['POST'])
def cancel_match():
    gid = get_id()
    r.lrem('casualZ', 0, gid)
    r.lrem('casualP', 0, gid)
    r.lrem('rankedZ', 0, gid)
    r.lrem('rankedZ', 0, gid)
    return {
        "ty": "MatchCancelled"
    }
