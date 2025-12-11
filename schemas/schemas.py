FILE_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "method": {"type": "string"},
        "href": {"type": "string", "format": "uri"},
        "templated": {"type": "boolean"},
        "operation_id": {"type": ["string", "null"]},
    },
    "required": ["method", "href", "templated"],
}

FILE_ERROR_SCHEMA = {
    "type": "object",
    "properties": {
        "error": {"type": "string"},
        "description": {"type": "string"},
        "message": {"type": "string"},
    },
    "required": ["error", "description", "message"],
}

FILES_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "limit": {"type": "integer"},
        "offset": {"type": "integer"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "type": {"type": "string"},
                    "name": {"type": "string"},
                    "created": {"type": "string"},
                    "modified": {"type": "string"},
                    "size": {"type": "integer"},
                    "mime_type": {"type": "string"},
                    "md5": {"type": "string"},
                    "sha256": {"type": "string"},
                    "preview": {"type": ["string", "null"], "format": "uri"},
                    "media_type": {"type": "string"},
                    "sizes": {
                        "type": ["array", "null"],
                        "items": {
                            "type": "object",
                            "properties": {
                                "url": {"type": "string", "format": "uri"},
                                "name": {"type": "string"},
                            },
                            "required": ["url", "name"],
                        },
                    },
                    "resource_id": {"type": "string"},
                    "revision": {"type": "integer"},
                    "comment_ids": {
                        "type": "object",
                        "properties": {
                            "public_resource": {"type": "string"},
                            "private_resource": {"type": "string"},
                        },
                        "required": ["public_resource", "private_resource"],
                    },
                    "exif": {"type": "object"},
                    "antivirus_status": {"type": "string"},
                    "file": {"type": "string", "format": "uri"},
                },
                "required": [
                    "path",
                    "type",
                    "name",
                    "created",
                    "modified",
                    "size",
                    "mime_type",
                    "md5",
                    "sha256",
                    "media_type",
                    "resource_id",
                    "revision",
                    "comment_ids",
                    "exif",
                    "antivirus_status",
                    "file",
                ],
            },
        },
    },
    "required": ["limit", "items", "offset"],
}
