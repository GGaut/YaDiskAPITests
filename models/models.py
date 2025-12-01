from pydantic import BaseModel


class User(BaseModel):
    login: str
    display_name: str


class DiskInfoResponse(BaseModel):
    user: User


class DI_ErrorResponse(BaseModel):
    error: str
    description: str
    message: str
