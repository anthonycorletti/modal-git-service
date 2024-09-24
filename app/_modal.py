import json
from typing import Dict

from fastapi import FastAPI
from modal import App, Image, Secret, Volume, asgi_app

from app.settings import settings

label = "git-on-modal"

app = App(name=label)

_app_env_dict: Dict[str, str | None] = {
    f"APP_{str(k)}": str(v) for k, v in json.loads(settings.model_dump_json()).items()
}
app_env = Secret.from_dict(_app_env_dict)


image = (
    Image.debian_slim()
    .pip_install("uv")
    .workdir("/work")
    .copy_local_file("pyproject.toml", "/work/pyproject.toml")
    .copy_local_file("uv.lock", "/work/uv.lock")
    .env({"UV_PROJECT_ENVIRONMENT": "/usr/local"})
    .run_commands(
        "apt-get update -y",
        "apt-get install -y git",
        "apt clean -y",
        "rm -rf /var/lib/apt/lists/*",
        "uv sync --frozen --compile-bytecode",
        "uv build",
    )
)


@app.function(
    image=image,
    secrets=[app_env],
    volumes={
        settings.GIT_HOME: Volume.from_name(
            label=f"{label}-BB7012EF-CFA1-4942-A226-37DB52CE0709",
            create_if_missing=True,
        )
    },
)
@asgi_app(label=label)
def _app() -> FastAPI:
    from app.main import app as main_app

    return main_app
