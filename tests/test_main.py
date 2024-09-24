import subprocess

from httpx import AsyncClient

from app.settings import settings


async def test_repository(client: AsyncClient) -> None:
    response = await client.post(
        "/repositories", json={"owner_name": "test", "repository_name": "test"}
    )
    assert response.status_code == 200

    response = await client.get("/repositories?owner_name=test")
    assert response.status_code == 200
    assert response.json() == {"repositories": ["test/test.git"]}

    response = await client.delete(
        "/repositories?owner_name=test&repository_name=test",
    )
    assert response.status_code == 200

    response = await client.get("/repositories?owner_name=test")
    assert response.status_code == 200
    assert response.json() == {"repositories": []}

    # delete the files
    subprocess.run(f"rm -rf {settings.GIT_HOME}/test", shell=True)
