import logging
import traceback

from fastapi import APIRouter, Response, status

from src.domains.llm_agent.app.requests.schemas import PostChatRequest, PostChatResponse
from src.infrastructure.graph.graph import GenerateAnalystsGraph
from src.schemas.common import ResponseBase

router = APIRouter(
    prefix="/llm_agent",
    tags=["chat_with_persona"]
)


@router.post("/generate_analysts",
             response_model=PostChatResponse,
             status_code=status.HTTP_200_OK)
async def chat_interaction(response: Response,
                           generate_analysts_data: PostChatRequest):
    logging.debug(f"Request generate analysts: {generate_analysts_data}")
    graph = GenerateAnalystsGraph()
    try:
        chat_response = await graph.process(generate_analysts_data)
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
