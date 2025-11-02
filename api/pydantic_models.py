from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(LoginRequest):
    password_confirmation: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
