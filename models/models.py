from dataclasses import dataclass
from typing import Any, Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class FileResponse:
    method: str
    href: str
    templated: bool
    operation_id: Optional[str] = None


@dataclass_json
@dataclass
class FileError:
    error: str
    description: str
    message: str


# List of files response
@dataclass_json
@dataclass
class Size:
    url: str
    name: str


@dataclass_json
@dataclass
class CommentIds:
    public_resource: str
    private_resource: str


@dataclass_json
@dataclass
class Item:
    path: str
    type: str
    name: str
    created: str
    modified: str
    size: int
    mime_type: str
    md5: str
    sha256: str
    media_type: str
    resource_id: str
    revision: int
    comment_ids: CommentIds
    exif: dict[str, Any]
    antivirus_status: str
    file: str
    preview: Optional[str] = None
    sizes: Optional[list[Size]] = None


@dataclass_json
@dataclass
class FilesResponse:
    limit: int
    items: list[Item]
    offset: int
