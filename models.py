from pydantic import BaseModel


class UploadRequestBody(BaseModel):
    level_data: str
    level_id: str
    level_name: str
    level_author: str
    level_tags: str


class UploadResponseBody(BaseModel):
    status: str
    attachment_id: int | None = None
