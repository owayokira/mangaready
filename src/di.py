from typing import AsyncGenerator

from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from starlette.requests import Request

from src.config import Config
from src.domain import interfaces, usecases
from src.infrastructures import repositories, services


class SQLAlchemyProvider(Provider):
    def __init__(self, engine: AsyncEngine, scope: Scope | None = None) -> None:
        super().__init__(scope)
        self._engine = engine

    @provide(scope=Scope.REQUEST)
    async def session(self, request: Request) -> AsyncGenerator[AsyncSession, None]:
        async with request.app.state.session_factory() as session:
            yield session


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def uow(
        self,
        user_repository: interfaces.UserRepositoryProtocol,
        session: AsyncSession,
    ) -> interfaces.UnitOfWorkProtocol:
        return repositories.SQLAlchemyUnitOfWork(user_repository, session)

    @provide(scope=Scope.REQUEST)
    async def user_repository(
        self,
        session: AsyncSession,
    ) -> interfaces.UserRepositoryProtocol:
        return repositories.SQLAlchemyUserRepository(session)


class ServiceProvider(Provider):
    def __init__(self, config: Config, scope: Scope | None = None) -> None:
        super().__init__(scope)
        self._config = config

    @provide(scope=Scope.APP)
    def sha256_password_hasher(self) -> interfaces.PasswordHasherProtocol:
        return services.SHA256PasswordHasher(
            self._config.security.password_hash_pepper,
            self._config.security.password_hash_count,
        )


class UsecaseProvider(Provider):
    scope = Scope.REQUEST
    register_user_usecase = provide(usecases.RegisterUserUsecase)


def configure_dependencies(app: FastAPI, config: Config) -> None:
    engine = create_async_engine(config.db.uri.get_secret_value())

    container = make_async_container(
        FastapiProvider(),
        SQLAlchemyProvider(engine),
        RepositoryProvider(),
        ServiceProvider(config),
        UsecaseProvider(),
    )
    setup_dishka(container, app)

    @app.on_event("shutdown")
    async def shutdown_event():
        await engine.dispose()
