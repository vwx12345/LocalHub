
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


PostCategory = Literal[
    "restaurant",
    "tour",
    "free",
]


class PostCreate(BaseModel):
    category: PostCategory = "free"

    title: str = Field(
        min_length=1,
        max_length=200,
    )

    content: str = Field(
        min_length=1,
    )

    password: str = Field(
        min_length=1,
        max_length=100,
    )


class PostUpdate(BaseModel):
    category: PostCategory = "free"

    title: str = Field(
        min_length=1,
        max_length=200,
    )

    content: str = Field(
        min_length=1,
    )

    password: str = Field(
        min_length=1,
        max_length=100,
    )


class PostDelete(BaseModel):
    password: str


class PostResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    category: PostCategory
    title: str
    content: str
    views: int
    created_at: datetime
    updated_at: datetime
