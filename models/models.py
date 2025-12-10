from typing import Any, Optional

from pydantic import BaseModel, Field, HttpUrl


# Trash response
class TrashItem(BaseModel):
    path: str
    name: str


class EmbeddedTrash(BaseModel):
    items: list[TrashItem]


class TrashResponse(BaseModel):
    embedded: EmbeddedTrash = Field(alias="_embedded")


# File operation response
class FileError(BaseModel):
    error: str
    description: str
    message: str


class FileResponse(BaseModel):
    method: str
    href: HttpUrl
    templated: bool
    operation_id: Optional[str] = None


# List of files response
class Size(BaseModel):
    url: HttpUrl
    name: str


class CommentIds(BaseModel):
    public_resource: str
    private_resource: str


class Item(BaseModel):
    path: str
    type: str
    name: str
    created: str
    modified: str
    size: int
    mime_type: str
    md5: str
    sha256: str
    preview: Optional[HttpUrl] = None
    media_type: str
    sizes: Optional[list[Size]] = None
    resource_id: str
    revision: int
    comment_ids: CommentIds
    exif: dict[str, Any]
    antivirus_status: str
    file: HttpUrl


class FilesResponse(BaseModel):
    limit: int
    items: list[Item]
    offset: int
