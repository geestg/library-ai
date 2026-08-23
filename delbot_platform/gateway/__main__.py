import uvicorn

from delbot_platform.core.config_manager import ConfigManager


def main():

    cfg = ConfigManager()

    gateway = cfg.service("gateway")

    uvicorn.run(
        "delbot_platform.gateway.app:app",
        host="0.0.0.0",
        port=gateway["port"],
        reload=False,
    )


if __name__ == "__main__":
    main()