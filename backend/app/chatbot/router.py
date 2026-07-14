from fastapi import APIRouter, HTTPException
from openai import APIConnectionError, AuthenticationError, RateLimitError

from app.chatbot.schema import ChatRequest, ChatResponse
from app.chatbot.service import create_chat_response


router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"],
)


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
) -> ChatResponse:
    try:
        return await create_chat_response(request)

    except AuthenticationError as error:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API 인증 설정에 문제가 있습니다.",
        ) from error

    except RateLimitError as error:
        raise HTTPException(
            status_code=429,
            detail="요청이 많습니다. 잠시 후 다시 시도해주세요.",
        ) from error

    except APIConnectionError as error:
        raise HTTPException(
            status_code=503,
            detail="AI 서비스에 연결할 수 없습니다.",
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="챗봇 답변 생성에 실패했습니다.",
        ) from error