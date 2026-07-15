import subprocess

from pathlib import Path


class RuntimeProcess:

    def __init__(self):

        self.process = None

    def start(
        self,
        command: list[str],
        cwd: Path,
    ):

        self.process = subprocess.Popen(
            command,
            cwd=cwd,
        )

        return self.process.pid

    def stop(self):

        if self.process:

            self.process.terminate()

    @property
    def pid(self):

        if self.process:

            return self.process.pid

        return None