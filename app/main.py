import os

import structlog
from fastapi import FastAPI
from fastapi.routing import APIRoute

from app import __version__
from app.git.middleware import GitMiddleware
from app.logging import configure_logging
from app.router import router
from app.settings import settings

log = structlog.get_logger()
os.environ["TZ"] = "UTC"


def generate_unique_openapi_id(route: APIRoute) -> str:
    return f"{route.tags[0]}:{route.name}"


def add_git_middleware(app: FastAPI) -> None:
    app.add_middleware(GitMiddleware)


def create_app() -> FastAPI:
    if not os.path.exists(settings.GIT_HOME):
        os.makedirs(settings.GIT_HOME)
    app = FastAPI(
        title="modal-git-service",
        generate_unique_id_function=generate_unique_openapi_id,
        version=__version__,
    )
    add_git_middleware(app)
    app.include_router(router)
    return app


configure_logging()
app = create_app()
