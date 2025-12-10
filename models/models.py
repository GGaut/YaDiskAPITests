from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


# Trash response
class TrashItem(BaseModel):
    path: str
    name: str


class EmbeddedTrash(BaseModel):
    items: list[TrashItem]


class TrashResponse(BaseModel):
    embedded: EmbeddedTrash = Field(alias="_embedded")


# File opreation response
class FileResponse(BaseModel):
    method: str
    href: HttpUrl
    templated: bool
    operation_id: Optional[str] = None


class FileError(BaseModel):
    error: str
    description: str
    message: str
