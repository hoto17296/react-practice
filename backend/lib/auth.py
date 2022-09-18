import re
from hashlib import pbkdf2_hmac
from logging import getLogger
from aiohttp import web
from aiohttp.abc import AbstractView
from aiohttp_session import get_session
from models import User

logger = getLogger(__name__)


def middleware(salt: bytes):
    @web.middleware
    async def auth_middleware(request, handler):
        session = await get_session(request)
        request["auth"] = await Auth.create(session, request.app["pg"], salt)
        return await handler(request)

    return auth_middleware


def required(func):
    async def wrapper(*args, **kwargs):
        # Supports class based views
        request = args[0].request if isinstance(args[0], AbstractView) else args[0]
        if request["auth"].user is None:
            raise web.HTTPUnauthorized()
        return await func(*args, **kwargs)

    return wrapper


def password_hash(password: str, salt: bytes) -> str:
    return pbkdf2_hmac("sha256", password.encode(), salt, 100000).hex()


class Auth:
    def __init__(self, session, pg, salt):
        self.session = session
        self.pg = pg
        self.salt = salt
        self.user: User | None = None

    @classmethod
    async def create(cls, *args, **kwargs):
        self = cls(*args, **kwargs)
        self.user = await self.get_user()
        return self

    async def get_user(self) -> User:
        user_id = self.session.get("user_id")
        if user_id is None:
            return None
        return await User.fetch(self.pg, user_id)

    async def check_email_used(self, email: str) -> bool:
        return bool(await User.fetchFromEmail(self.pg, email))

    async def register(self, email: str, password: str, **kwargs):
        # Validation
        errors = []
        if len(email) == 0:
            errors.append(("email", "Email is empty."))
        elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email, flags=re.ASCII):
            errors.append(("email", "Invalid email address format."))
        elif await self.check_email_used(email):
            errors.append(("email", "This email has already used."))
        if len(password) == 0:
            errors.append(("password", "Password is empty."))
        elif len(password) < 8:
            errors.append(("password", "Password should be at least 8 characters."))
        elif not re.match(r"^[\x21-\x7e]+$", password):
            errors.append(("password", "Password should be ASCII string."))
        if len(errors) > 0:
            raise ValueError(*errors)

        return await User.create(
            self.pg,
            email=email,
            password_hash=password_hash(password, self.salt),
            **kwargs,
        )

    def verify_password(self, user: User, password: str) -> bool:
        return user.password_hash == password_hash(password, self.salt)

    def set_session(self, user: User):
        self.session["user_id"] = user.id

    def clear_session(self):
        self.session["user_id"] = None
