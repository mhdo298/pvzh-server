import os

from quart import Quart, current_app, request
from redis.asyncio import Redis, ConnectionPool

redis_url = os.getenv('REDIS_URL')

redis_initialized = False
def init_redis(app: Quart):
    global redis_initialized
    if not redis_initialized:
        redis_initialized = True
        @app.while_serving
        async def setup_redis():
            current_app.redis_pool = ConnectionPool.from_url(redis_url, max_connections=1)
            yield
            await current_app.redis_pool.aclose()

        @app.before_request
        async def make_redis():
            request.redis = Redis(connection_pool=current_app.redis_pool)


        @app.teardown_request
        async def clean_redis(_):
            await request.redis.aclose()
