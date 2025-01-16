from flask import Blueprint, request

from utils import get_id

seasons = Blueprint('seasons', __name__, url_prefix='/seasons')

@seasons.route('/<version>/history')
def history(version):
   return {
        "seasons": {},
        "version": None,
        "id": get_id()
    }
# @seasons.route('/<path:version>/complete', methods=['POST'])
# def complete(version):
#     return {
#         "current": {
#             "gamesPlayed": 0,
#             "stars": 0,
#             "id": get_id(),
#             "version": 1,
#             "season": "",
#             "wins": 0,
#             "losses": 0,
#             "mmr": 1600,
#             "rank": 1,
#             "streakBonus": 0,
#             "wonLastGame": False
#         },
#         "history": {
#             "seasons": {},
#             "version": 1,
#             "id": get_id()
#         }
#     }


# @seasons.route('/acknowledge')
# def acknowledge():
#     return {}