import uuid

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.domain import dtos, usecases

auth_router = APIRouter(prefix="/api/auth")


@auth_router.post("/register")
@inject
async def register_user_handler(
    dto: dtos.RegisterUserDTO,
    usecase: FromDishka[usecases.RegisterUserUsecase],
) -> dtos.RegisteredUserDTO:
    print("bla bla", usecase)
    return await usecase.execute(dto)
