from passlib.hash import pbkdf2_sha256
from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, status, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer

from api.db import engine
from api.models import create_all
from api.depends import session_dep
from api.pydantic_models import LoginRequest, LoginResponse, RegisterRequest
from api.config import config
from api import crud


def hash_password(password: str) -> str:
    hashed_password = pbkdf2_sha256.hash(password)
    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed_password)


@AuthJWT.load_config
def get_jwt_config():
    return [("authjwt_secret_key", config.SECRET_KEY)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all(engine)
    yield


app = FastAPI(debug=True, lifespan=lifespan)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.post("/register")
async def register(session=session_dep, register_data: RegisterRequest = Body(...)):
    existing_user = await crud.get_user_by_username(
        session, username=register_data.username
    )
    if existing_user is not None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"User: {register_data.username} already exists.",
        )

    if register_data.password != register_data.password_confirmation:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Passwords doesn't match.",
        )

    username = register_data.username
    password_digest = hash_password(register_data.password)
    if not await crud.store_new_user(session, username=username, password_digest=password_digest):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Failed to save new user.",
        )


@app.post("/login")
async def login(
    session=session_dep,
    login_data: LoginRequest = Body(...),
    authorize: AuthJWT = Depends(AuthJWTBearer()),
):
    user = await crud.get_user_by_username(session, username=login_data.username)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials.")
    access_token = await authorize.create_access_token(subject=user.username)
    refresh_token = await authorize.create_refresh_token(subject=user.username)
    return LoginResponse(access_token=access_token, refresh_token=refresh_token)


@app.post("/refresh")
async def refresh(authorize: AuthJWT = Depends(AuthJWTBearer())):
    await authorize.jwt_refresh_token_required()
    current_user = await authorize.get_jwt_subject()
    new_access_token = await authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@app.get("/protected")
async def protected(authorize: AuthJWT = Depends(AuthJWTBearer())):
    await authorize.jwt_required()

    current_user = await authorize.get_jwt_subject()
    return {"user": current_user}
