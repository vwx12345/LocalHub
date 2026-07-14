from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000,
    )

    previous_response_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    response_id: str