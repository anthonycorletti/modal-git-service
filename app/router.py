from fastapi import APIRouter

from app.git.router import router as git_router
from app.repositories.router import router as repositories_router

router = APIRouter()

# /git
router.include_router(git_router, tags=["git"])

# /repositories
router.include_router(repositories_router, tags=["repositories"])
