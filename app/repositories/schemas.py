from pydantic import BaseModel


class Repository(BaseModel):
    owner_name: str
    repository_name: str
    initial_branch: str = "main"
