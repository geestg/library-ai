from __future__ import annotations


import subprocess


from pathlib import Path


from delbot_platform.ai.process.process_info import (
    ProcessInfo,
)

from delbot_platform.ai.process.process_monitor import (
    ProcessMonitor,
)

from delbot_platform.ai.process.process_registry import (
    ProcessRegistry,
)



class ProcessManager:


    def __init__(self):

        self.registry = ProcessRegistry()

        self.monitor = ProcessMonitor()



    def start(
        self,
        *,
        name: str,
        command: list[str],
        workdir: Path,
        host="127.0.0.1",
        port=0,
    ):


        process = subprocess.Popen(
            command,
            cwd=workdir,
        )


        info = ProcessInfo(

            name=name,

            command=command,

            workdir=workdir,

            pid=process.pid,

            process=process,

            running=True,

            host=host,

            port=port,

        )


        self.registry.register(
            info
        )


        return info



    def stop(
        self,
        name:str,
    ):


        info = self.registry.get(
            name
        )


        if info is None:

            return False


        if info.process:

            info.process.terminate()


        info.running=False


        self.registry.register(
            info
        )


        return True



    def get(
        self,
        name:str,
    ):


        info=self.registry.get(
            name
        )


        if info:

            return self.monitor.refresh(
                info
            )


        return None



    def list(self):

        return [

            self.monitor.refresh(
                x
            )

            for x in self.registry.list()

        ]
