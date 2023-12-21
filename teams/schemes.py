from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserScheme(BaseModel):
    name: str
    password: str
    email: str
    role: str


class MessageScheme(BaseModel):
    receiver: str
    content: str


class LoginRequest(BaseModel):
    username: str
    password: str
