from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse

from api.db import engine
from api.models import create_all
from api.depends import session_dep
from api.pydantic_models import LoginModel, LoginResponse
from api import crud


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all(engine)
    yield


app = FastAPI(debug=True, lifespan=lifespan)


@app.post("/login", response_model=LoginResponse)
async def login(session = session_dep, login_data: LoginModel = Body(...)):
    user = await crud.get_user_by_username(session, username=login_data.username)
    if user is None:
        return JSONResponse(LoginResponse(msg=f"User: '{login_data.username}' not found."), status.HTTP_404_NOT_FOUND)
    return JSONResponse(LoginResponse(msg="it's working!"), status.HTTP_200_OK)
