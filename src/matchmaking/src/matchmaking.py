import json
from random import getrandbits

from flask import Blueprint, request
from cache import r, get_or_default
from utils import get_id

matchmaking = Blueprint('matchmaking', __name__, url_prefix='/matchmaking')


@matchmaking.route('/<version>/queryStats', methods=['POST'])
def query_stats(version):
    return {
        "fastestRankedMatch": "None",
        "fastestCasualMatch": "None"
    }


@matchmaking.route('/<version>/createChallenge', methods=['POST'])
def create_challenge(version):
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


@matchmaking.route('/<version>/makeMatch', methods=['POST'])
def make_match(version):
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


@matchmaking.route('/<version>/cancelMatch', methods=['POST'])
def cancel_match(version):
    pid = get_id()
    r.lrem('casualZ', 0, pid)
    r.lrem('casualP', 0, pid)
    r.lrem('rankedZ', 0, pid)
    r.lrem('rankedZ', 0, pid)
    return {
        "ty": "MatchCancelled"
    }


@matchmaking.route('/<version>/matchPoll', methods=['POST'])
def match_poll(version):
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


@matchmaking.route('/<version>/joinMatch', methods=['POST'])
def join_match(version):
    data = request.get_json()
    gi = data['gi']
    sd = get_or_default(gi + "-sd", r.get, b'').decode()
    return {
        "ty": "MatchReady",
        "sd": sd,
        "gi": gi,
        "or": 1
    }
