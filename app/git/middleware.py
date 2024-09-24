from fastapi import FastAPI
from starlette.types import Receive, Scope, Send


class GitMiddleware:
    def __init__(self, app: FastAPI) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if "headers" not in scope.keys():
            await self.app(scope, receive, send)
            return

        _user_agent = [
            _header[1] for _header in scope["headers"] if _header[0] == b"user-agent"
        ]
        if _user_agent and _user_agent[0].startswith(b"git/"):
            scope["path"] = f"/git{scope['path']}"

        await self.app(scope, receive, send)
