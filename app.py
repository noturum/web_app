import asyncio
import logging
import sys
import uvicorn
from fastapi import FastAPI

from models.base import db_controller
from main.page import api


def run_web():
    app = FastAPI()
    app.include_router(api)
    uvicorn.run(app=app, port=80)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.get_event_loop().set_debug(True)
    with asyncio.Runner() as r:
        r.run(db_controller.bootstrap())
        r.get_loop().run_in_executor(None, run_web)
