from fastapi import FastAPI

from src.config import gather_config


def create_app() -> FastAPI:
    config = gather_config()
    app = FastAPI(debug=config.debug)

    return app
