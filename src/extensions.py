from abc import ABCMeta, abstractmethod

import sqlalchemy as sa
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import registry

from src.domain import models


class FastAPIExtension(metaclass=ABCMeta):
    @abstractmethod
    def configure(self, app: FastAPI) -> None:
        ...


class SQLAlchemyExtension(FastAPIExtension):
    def __init__(self, uri: str) -> None:
        self._uri = uri

    def configure(self, app: FastAPI) -> None:
        engine = create_async_engine(self._uri)
        app.state.engine = engine

        session_factory = async_sessionmaker(engine, expire_on_commit=False)
        app.state.session_factory = session_factory

        @app.on_event("startup")
        async def on_startup() -> None:
            app.state.registry = create_mapper_registry()


        @app.on_event("shutdown")
        async def _on_shutdown_lifespan_handler() -> None:
            await app.state.engine.dispose()
            app.state.registry.dispose()

def _create_user_table(metadata: sa.MetaData) -> sa.Table:
    return sa.Table(
        'user',
        metadata,
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('username', sa.String(32), unique=True, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('password_salt', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, default=sa.func.now()),
        sa.Column(
            'updated_at', sa.TIMESTAMP, nullable=False,
            default=sa.func.now(), onupdate=sa.func.now(),
        ),
    )


def create_mapper_registry() -> registry:
    mapper_registry = registry()

    user_table = _create_user_table(mapper_registry.metadata)
    mapper_registry.map_imperatively(models.UserStorage, user_table)

    return mapper_registry
