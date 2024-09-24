import os
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Body, Query
from fastapi.responses import JSONResponse

from app.git.service import GitService
from app.repositories.schemas import Repository
from app.settings import settings

router = APIRouter()


class Routes:
    create = "/repositories"
    delete = "/repositories"
    list = "/repositories"


@router.post(Routes.create, response_class=JSONResponse)
async def _create_repository(
    create_repository_query: Annotated[Repository, Body()],
) -> JSONResponse:
    _path = Path(
        f"{settings.GIT_HOME}/{create_repository_query.owner_name}/"
        f"{create_repository_query.repository_name}.git"
    )
    if not _path.exists():
        GitService.init(_path, create_repository_query.initial_branch)
    return JSONResponse(content={"message": "success"})


@router.delete(Routes.delete, response_class=JSONResponse)
async def _delete_repository(
    create_repository_query: Annotated[Repository, Query()],
) -> JSONResponse:
    os.system(
        f"rm -rf {settings.GIT_HOME}/{create_repository_query.owner_name}/"
        f"{create_repository_query.repository_name}.git"
    )
    os.system("git update-server-info")
    return JSONResponse(content={"message": "success"})


@router.get(Routes.list, response_class=JSONResponse)
async def _list_repos_for_owner() -> JSONResponse:
    repos = []
    if os.path.exists(f"{settings.GIT_HOME}"):
        for owner in os.listdir(f"{settings.GIT_HOME}"):
            for repo in os.listdir(f"{settings.GIT_HOME}/{owner}"):
                repos.append(f"{owner}/{repo}")
    return JSONResponse(content={"repositories": repos})
