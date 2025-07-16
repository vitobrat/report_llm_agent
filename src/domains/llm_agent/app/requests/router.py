import logging
import traceback

from fastapi import APIRouter, Response, status

from src.domains.llm_agent.app.requests.schemas import PostGenerateAnalystsRequest, PostInterviewingRequest, \
    PostGenerateAnalystsResponse, PostInterviewingResponse, PostResearchResponse, PostResearchRequest
from src.infrastructure.graphs.generate_analysts.graph import GenerateAnalystsGraph
from src.infrastructure.graphs.interviewing.graph import InterviewingGraph
from src.infrastructure.graphs.research.graph import ResearchGraph
from src.schemas.common import ResponseBase

router = APIRouter(
    prefix="/llm_agent",
    tags=["report_generate"]
)


@router.post("/generate_analysts",
             response_model=PostGenerateAnalystsResponse,
             status_code=status.HTTP_200_OK)
async def generate_analysts(response: Response,
                           generate_analysts_data: PostGenerateAnalystsRequest):
    logging.debug(f"Request generate analysts: {generate_analysts_data}")
    graph = GenerateAnalystsGraph()
    try:
        generate_analysts_response = await graph.process(generate_analysts_data)
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        generate_analysts_response = None

    if generate_analysts_response is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseBase(
            details='Ошибка'
        )
    return PostGenerateAnalystsResponse(
        msg=generate_analysts_response if generate_analysts_response else None
    )

@router.post("/interviewing",
             response_model=PostInterviewingResponse,
             status_code=status.HTTP_200_OK)
async def interviewing(response: Response,
                       interviewing_data: PostInterviewingRequest):
    logging.debug(f"Request generate analysts: {interviewing_data}")
    graph = InterviewingGraph()
    try:
        interviewing_response = await graph.process(interviewing_data)
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        interviewing_response = None

    if interviewing_response is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseBase(
            details='Ошибка'
        )
    return PostInterviewingResponse(
        msg=interviewing_response if interviewing_response else None
    )

@router.post("/research",
             response_model=PostResearchResponse,
             status_code=status.HTTP_200_OK)
async def research(response: Response,
                   research_data: PostResearchRequest):
    logging.debug(f"Request generate analysts: {research_data}")
    graph = ResearchGraph()
    try:
        research_response = await graph.process(research_data)
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        research_response = None

    if research_response is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseBase(
            details='Ошибка'
        )
    return PostResearchResponse(
        msg=dict(research_response) if research_response else None
    )