from os import getenv
from asyncio import sleep
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage
import asyncpg
import aioredis
import lib.auth as auth
from views.index import routes as routes_index
from views.auth import routes as routes_auth


@web.middleware
async def cors_middleware(request, handler):
    headers = {
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Origin": getenv("CORS_ALLOW_ORIGIN", "*"),
    }
    if request.method == "OPTIONS":
        return web.Response(headers=headers)
    try:
        response = await handler(request)
        for key, value in headers.items():
            response.headers[key] = value
        return response
    except web.HTTPException as e:
        for key, value in headers.items():
            e.headers[key] = value
        raise e


cookie_params = {
    # `SameSite=None` required when frontend and backend are cross-site
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite
    "samesite": getenv("COOKIE_SAMESITE", "Lax"),
}

# `Secure` (HTTPS) required when `SameSite=None`
if cookie_params["samesite"] == "None":
    cookie_params["secure"] = True


app = web.Application(
    middlewares=[
        cors_middleware,
        session_middleware(RedisStorage(aioredis.from_url(getenv("REDIS_URL")), **cookie_params)),
        auth.middleware(getenv("AUTH_SALT").encode()),
    ]
)
app.add_routes(routes_index)
app.add_routes(routes_auth)


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
