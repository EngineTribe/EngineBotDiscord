from pydantic import BaseModel
from typing import Optional as Opt


class UploadRequestBody(BaseModel):
    level_data: str
    level_id: str
    level_name: str
    level_author: str
    level_author_im_id: int
    level_tags: str
    description: Opt[str] = 'Sin descripción'


class UploadResponseBody(BaseModel):
    status: str
    attachment_id: int | None = None


class ServerStats(BaseModel):
    os: str
    python: str
    player_count: int
    level_count: int
    uptime: int
    connection_per_minute: int
