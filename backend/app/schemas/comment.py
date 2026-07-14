from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentCreate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=1000,
    )
    password: str = Field(
        min_length=1,
        max_length=100,
    )

    # 일반 댓글은 null, 대댓글은 부모 댓글 ID
    parent_id: int | None = None


class CommentUpdate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=1000,
    )
    password: str = Field(
        min_length=1,
        max_length=100,
    )


class CommentDelete(BaseModel):
    password: str = Field(
        min_length=1,
        max_length=100,
    )


class CommentItemResponse(BaseModel):
    id: int
    post_id: int
    parent_id: int | None
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentResponse(CommentItemResponse):
    replies: list[CommentItemResponse] = Field(
        default_factory=list,
    )