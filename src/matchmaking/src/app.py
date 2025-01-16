from flask import Flask

from matchmaking import matchmaking
from seasons import seasons
from pvp import pvp
app = Flask(__name__)
HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
app.register_blueprint(matchmaking)
app.register_blueprint(seasons)
app.register_blueprint(pvp)

@app.route('/<path:path>', methods=HTTP_METHODS)
def catch_all(path):
    print(path)
    return ''
