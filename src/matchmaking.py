import json

from flask import Blueprint, request
from utils import r, it_should_be_there_soon
from random import getrandbits

matchmaking = Blueprint('matchmaking', __name__, url_prefix='/matchmaking/v1')


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


@matchmaking.route('/makeMatch')
def make_match():
    return {
        "ty": "WaitingForMatch",
        "eta": 30,
        "gi": None
    }


@matchmaking.route('/matchPoll')
def match_poll():
    return {}
