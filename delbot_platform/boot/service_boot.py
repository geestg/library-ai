from __future__ import annotations


from delbot_platform.controller.service_controller import (
    ServiceController,
)


class ServiceBoot:


    BOOT_ORDER = [

        "embedding",

        "reranker",

        "vision",

        "ocr",


        "chat",

        "gateway",

        "research_api",

    ]


    def __init__(self) -> None:

        self.controller = ServiceController()



    def start(
        self,
        service: str,
    ):

        print()

        print(
            f"[BOOT] Starting {service}"
        )


        process = self.controller.start(
            service,
        )


        print(
            f"[BOOT] PID {process.pid}"
        )


        return process



    def boot(self):

        processes = []


        for service in self.BOOT_ORDER:


            process = self.start(
                service,
            )


            processes.append(
                process,
            )


        return processes
