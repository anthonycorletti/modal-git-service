import secrets
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.git.schemas import GitPackService
from app.git.service import GitService
from app.settings import settings

router = APIRouter(prefix="/git")
security = HTTPBasic()


# NOTE: for demo purposes obviously, do not use this in production
def basic_auth(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    username = secrets.compare_digest(
        credentials.username, settings.DEFAULT_GIT_USERNAME
    )
    password = secrets.compare_digest(
        credentials.password, settings.DEFAULT_GIT_PASSWORD
    )
    if not (username and password):
        raise HTTPException(status_code=401)
    return credentials.username


@router.get("/{path:path}/info/refs", response_class=StreamingResponse)
async def _inforefs(
    path: str, service: GitPackService, user: str = Depends(basic_auth)
) -> StreamingResponse:
    _path = Path(settings.GIT_HOME, path)

    # Create repo if does does not exist
    git_repo = GitService(_path) if _path.exists() else GitService.init(_path)

    # Fetch inforefs
    data = git_repo.inforefs(service.value)

    media = f"application/x-{service.value}-advertisement"
    return StreamingResponse(data, media_type=media)


@router.post("/{path:path}/{service}", response_class=StreamingResponse)
async def _service(
    path: str, service: GitPackService, req: Request
) -> StreamingResponse:
    git_repo = GitService(Path(settings.GIT_HOME, path))

    # Load data to memory (be careful with huge repos)
    stream = req.stream()
    data = b"".join([data async for data in stream])

    # Load service data
    service_data = git_repo.service(service.value, data)

    media = f"application/x-{service.value}-result"
    return StreamingResponse(service_data, media_type=media)
