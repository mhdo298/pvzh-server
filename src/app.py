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

    @app.route("/<path:path>", methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
    async def catch(path):
        print(f'Uncaught path: {path}')
        print(request.method)
        return ''

    return app
