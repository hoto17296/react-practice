from os import getenv
from asyncio import sleep
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage
import asyncpg
import aioredis
from views.index import routes as routes_index

app = web.Application(middleware=[session_middleware(RedisStorage(aioredis.from_url(getenv("REDIS_URL"))))])
app.add_routes(routes_index)


async def startup(app: web.Application):
    e = None
    for i in range(5):
        try:
            await sleep(i)
            app["pg"] = await asyncpg.create_pool(dsn=getenv("DATABASE_URL"))
            break
        except ConnectionError as _e:
            e = _e
    else:
        raise e


async def cleanup(app: web.Application):
    await app["pg"].close()


app.on_startup.append(startup)
app.on_cleanup.append(cleanup)
