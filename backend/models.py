from logging import getLogger
from pydantic import BaseModel

logger = getLogger(__name__)


class User(BaseModel):
    id: int
    email: str
    password_hash: str = None

    @classmethod
    async def fetch(cls, pg, user_id: str) -> "User | None":
        query = f"""
            SELECT *
            FROM users
            WHERE user_id = $1
            """
        row = await pg.fetchrow(query, user_id)
        return cls(**row) if row else None

    @classmethod
    async def fetchFromEmail(cls, pg, email: str) -> "User | None":
        query = f"""
            SELECT *
            FROM users
            WHERE email = $1
            """
        row = await pg.fetchrow(query, email)
        return cls(**row) if row else None

    @classmethod
    async def create(cls, pg, email: str, password_hash: str) -> "User":
        query = f"""
            INSERT
            INTO users(email, password_hash)
            VALUES ($1, $2)
            """
        await pg.execute(query, email, password_hash)
        return await cls.fetchFromEmail(pg, email)
