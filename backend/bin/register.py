"""
Usage:
  docker compose exec -e PYTHONPATH=/app backend python bin/register.py {email} {password}
"""

import argparse
from os import getenv
import asyncio
import asyncpg
from lib.auth import Auth


async def register(email: str, password: str):
    auth = Auth(
        session=None,
        pg=await asyncpg.create_pool(dsn=getenv("DATABASE_URL")),
        salt=getenv("AUTH_SALT").encode(),
    )
    return await auth.register(email, password)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("email")
    parser.add_argument("password")
    args = parser.parse_args()

    loop = asyncio.get_running_loop()
    user = loop.run_until_complete(register(args.email, args.password))
    print(f"User registered successfully (id: {user.id})")
