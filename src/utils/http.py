from asyncio import gather

import orjson as json
import time

import aiohttp
from aiofiles import os, open
import os as _os
from quart import Quart, current_app

initialized = False


def init_http(app: Quart):
    global initialized
    if not initialized:
        initialized = True

        @app.while_serving
        async def setup_http():
            connector = aiohttp.TCPConnector(limit=100)
            jar = aiohttp.DummyCookieJar()
            app.http = aiohttp.ClientSession(connector=connector, cookie_jar=jar)
            yield
            await app.http.close()


async def get_json(url, local, check=True):
    exists = await os.path.exists(local)
    if not check and exists:
        async with open(local, 'rb') as f:
            return json.loads(await f.read())
    else:
        if exists:
            headers = {
                'If-Modified-Since': time.strftime('%a, %d %b %Y %H:%M:%S GMT',
                                                   time.gmtime(await os.path.getmtime(local)))}
        else:
            headers = None

        async with current_app.http.get(url, headers=headers) as resp:
            if resp.status == 304:
                async with open(local, 'rb') as f:
                    return json.loads(await f.read())
            else:
                content, _ = await gather(resp.json(content_type=None), os.makedirs(_os.path.dirname(local), exist_ok=True))
                async with open(local, mode='wb') as f:
                    await f.write(json.dumps(content))
                return content
