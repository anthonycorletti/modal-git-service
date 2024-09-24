from enum import Enum, unique


@unique
class GitPackService(str, Enum):
    receive = "git-receive-pack"
    upload = "git-upload-pack"
