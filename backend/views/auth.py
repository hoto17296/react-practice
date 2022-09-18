from logging import getLogger
import json
from asyncio import sleep
from aiohttp import web
from pydantic import BaseModel
import lib.auth as auth
from models import User

logger = getLogger(__name__)

routes = web.RouteTableDef()


class SigninFormInput(BaseModel):
    email: str
    password: str


@routes.post("/auth/signin")
async def signin(request):
    data = await request.json()
    try:
        data = SigninFormInput(**data)
    except:
        logger.warning("Invalid input format")
        logger.warning(data)
        raise web.HTTPBadRequest

    user = await User.fetchFromEmail(request.app["pg"], data.email)
    if user is None:
        await sleep(3)  # If signin fails, wait 3 seconds before response
        return web.json_response({"verified": False})

    verified = request["auth"].verify_password(user, data.password)

    if verified:
        request["auth"].set_session(user)
    else:
        await sleep(3)  # # If signin fails, wait 3 seconds before response

    return web.json_response({"verified": verified})


@routes.post("/auth/signout")
async def signout(request):
    request["auth"].clear_session()
    return web.json_response("")


@routes.post("/auth/register")
async def register(request):
    data = await request.json()
    try:
        await request["auth"].register(**data)
    except ValueError as e:
        logger.info("Error occurred when user registration", exc_info=True)
        raise web.HTTPBadRequest(text=json.dumps({"errors": e.args[0]}), content_type="application/json")

    return web.json_response("")


@routes.get("/auth/info")
@auth.required
async def get_info(request):
    user = request["auth"].user
    return web.json_response(
        {
            "user": {
                "email": user.email,
            },
        },
    )
