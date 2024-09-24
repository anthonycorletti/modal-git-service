import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import Request
from httpx import AsyncClient

from app.main import app
from app.settings import settings

TEST_BASE_URL = "http://testserver:8001"


@pytest_asyncio.fixture(scope="session", autouse=True)
def event_loop(request: Request) -> Generator[asyncio.AbstractEventLoop, None, None]:
    os.system(f"rm -rf {settings.GIT_HOME}")
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    # delete the contents of the GIT_HOME
    loop.close()
    os.system(f"rm -rf {settings.GIT_HOME}")


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator:
    async with LifespanManager(app) as manager:
        async with (
            AsyncClient(app=manager.app, base_url=TEST_BASE_URL) as client,
        ):
            yield client
