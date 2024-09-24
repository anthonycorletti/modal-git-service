import io
from pathlib import Path
from subprocess import PIPE, Popen, run
from typing import IO


class GitService:
    def __init__(self, path: Path) -> None:
        self.path = path

    @staticmethod
    def init(path: Path, initial_branch: str = "main") -> "GitService":
        run(
            ["git", "init", "--bare", f"--initial-branch={initial_branch}", path],
            check=True,
        )
        return GitService(path)

    def inforefs(self, service: str) -> IO:
        result = run(
            [service, "--stateless-rpc", "--advertise-refs", self.path],
            check=True,
            capture_output=True,
        )
        # Adapted from https://github.com/schacon/grack/blob/master/lib/grack.rb
        data = b"# service=" + service.encode()
        len_data = len(data) + 4
        datalen = b"%04x" % len_data
        data = datalen + data + b"0000" + result.stdout
        return io.BytesIO(data)

    def service(self, service: str, data: bytes) -> IO:
        proc = Popen([service, "--stateless-rpc", self.path], stdin=PIPE, stdout=PIPE)
        try:
            data, _ = proc.communicate(data)
        finally:
            proc.wait()
        return io.BytesIO(data)
