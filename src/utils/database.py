import os

from psycopg_pool import AsyncConnectionPool

from quart import Quart, request, current_app

initialized = False


def init_db(app: Quart):
    global initialized
    if not initialized:
        initialized = True

        @app.while_serving
        async def setup_db():
            current_app.db_pool = AsyncConnectionPool(conninfo=os.environ['POSTGRES_URL'])
            await current_app.db_pool.open()
            yield
            await current_app.db_pool.close()

        @app.before_request
        async def make_db():
            request.db = await current_app.db_pool.getconn()

        @app.teardown_request
        async def clean_db(_):
            await current_app.db_pool.putconn(request.db)
