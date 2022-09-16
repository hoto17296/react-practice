from logging import getLogger
from aiohttp import web

logger = getLogger(__name__)

routes = web.RouteTableDef()


@routes.get("/")
async def get_index(request):
    return web.json_response("ok")
