from fastapi import APIRouter

from src.schemas.users import UserRead, UserCreate, UserUpdate
from src.utils.auth_manager import fastapi_users, auth_backend

auth_router = APIRouter(
    prefix="",
    tags=["auth"],
)

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)