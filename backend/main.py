from os import getenv
import logging
from aiohttp import web
from app import app

logging.basicConfig(level=getenv("LOG_LEVEL", logging.WARNING))

if __name__ == "__main__":
    web.run_app(app, port=getenv("PORT", 8080))
