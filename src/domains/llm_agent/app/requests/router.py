import logging
import traceback

from fastapi import APIRouter, Response, status

from src.chat.chat import chat, scrap
from src.chat.domains.chat.app.requests.schemas import (
    PostChatRequest, PostChatResponse, Scrap
)
from src.chat.schemas.common import ResponseBase

router = APIRouter(
    prefix="/llm_agent",
    tags=["chat_with_persona"]
)


@router.post("/chat_response",
             response_model=PostChatResponse,
             status_code=status.HTTP_200_OK)
async def chat_interaction(response: Response,
                           chat_data: PostChatRequest):
    logging.debug(f"Request chat: {chat_data}")

    try:
        chat_response = await chat(data=chat_data)
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        chat_response = None

    if chat_response is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseBase(
            details='Ошибка'
        )
    return PostChatResponse(
        msg=chat_response if chat_response else None
    )


@router.post("/scrap",
             status_code=status.HTTP_200_OK)
async def scraping(response: Response,
                   data: Scrap):
    logging.debug(f"Request chat: {data}")

    try:
        scrap_response = await scrap(data=data)
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        scrap_response = None

    if scrap_response is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseBase(
            details='Ошибка'
        )
    return PostChatResponse(
        msg=scrap_response if scrap_response else None
    )
