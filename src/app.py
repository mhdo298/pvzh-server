from quart import Quart, request


def create_app():
    app = Quart(__name__)

    try:
        from src.assets.assets import register_assets
        register_assets(app)
    except ModuleNotFoundError:
        print('No assets')

    try:
        from src.persistence.persistence import register_persistence
        register_persistence(app)
    except ModuleNotFoundError:
        print('No persistence')

    try:
        from src.matchmaking.matchmaking import register_matchmaking
        register_matchmaking(app)
    except ModuleNotFoundError:
        print('No matchmaking')

    try:
        from src.seasons.seasons import register_seasons
        register_seasons(app)
    except ModuleNotFoundError:
        print('No seasons')

    try:
        from src.pvp.pvp import register_pvp
        register_pvp(app)
    except ModuleNotFoundError:
        print('No pvp')

    @app.before_request
    async def before_request():
        print(request.path)
        if request.method == 'POST':
            print(await request.get_json())

    @app.route("/<path:path>", methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
    async def catch(path):
        print(f'Uncaught path: {path}')
        print(request.method)
        return ''

    return app
