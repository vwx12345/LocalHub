from openai import AsyncOpenAI

from app.chatbot.schema import ChatRequest, ChatResponse
from app.core.config import get_settings


settings = get_settings()

client = AsyncOpenAI(
    api_key=settings.openai_api_key,
)


async def create_chat_response(
    request: ChatRequest,
) -> ChatResponse:
    response = await client.responses.create(
        model=settings.openai_model,
        instructions=(
            "너는 친절한 한국어 챗봇이다. "
            "사용자의 질문에 정확하고 이해하기 쉽게 답변한다."
        ),
        input=request.message,
        previous_response_id=request.previous_response_id,
    )

    return ChatResponse(
        answer=response.output_text,
        response_id=response.id,
    )