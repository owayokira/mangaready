import typing
from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.requests import Request

from src.config import gather_config
from src.di import configure_dependencies
from src.domain import exceptions
from src.extensions import SQLAlchemyExtension
from src.infrastructures import api


def create_app() -> FastAPI:
    config = gather_config()
    app = FastAPI(debug=config.server.debug)

    app.include_router(api.auth_router)
    SQLAlchemyExtension(config.db.uri.get_secret_value()).configure(app)

    configure_dependencies(app, config)

    @app.exception_handler(exceptions.ApplicationException)
    async def application_exception_handler(_: Request, exc: exceptions.ApplicationException) -> typing.NoReturn:
        exception_status_mapping: dict[type[exceptions.ApplicationException], int] = {
            exceptions.EmailAlreadyExistsException: HTTPStatus.CONFLICT,
            exceptions.UsernameAlreadyExistsException: HTTPStatus.CONFLICT,
        }

        raise HTTPException(status_code=exception_status_mapping[type(exc)], detail=exc.message)

    return app
