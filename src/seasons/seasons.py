from quart import Blueprint, request

from src.utils.misc import get_id

seasons = Blueprint('seasons', __name__, url_prefix='/<string:username>/<string:repo>/seasons')

def register_seasons(app):
    app.register_blueprint(seasons)

@seasons.route('/<version>/history')
def history(username, repo, version):
   return {
        "seasons": {},
        "version": None,
        "id": get_id()
    }

@seasons.route('/<path:version>/complete', methods=['POST'])
async def complete(username, repo, version):
    return {
        "current": {
            "gamesPlayed": 0,
            "stars": 0,
            "id": get_id(),
            "version": 1,
            "season": "season_79",
            "wins": 0,
            "losses": 0,
            "mmr": 1600,
            "rank": 50,
            "streakBonus": 0,
            "wonLastGame": False
        },
        "history": {
            "seasons": {},
            "version": 1,
            "id": get_id()
        }
    }

# @seasons.route('/acknowledge')
# def acknowledge(username, repo):
#     return {}