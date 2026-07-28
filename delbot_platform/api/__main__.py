from __future__ import annotations

import uvicorn

from delbot_platform.api.main import app


def main() -> None:

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8200,
    )


if __name__ == "__main__":
    main()
