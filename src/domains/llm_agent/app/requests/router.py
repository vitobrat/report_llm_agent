import logging
import traceback

from fastapi import APIRouter, Response, status
from fastapi.responses import StreamingResponse

from src.domains.llm_agent.app.requests.schemas import PostGenerateAnalystsRequest, PostInterviewingRequest, \
    PostGenerateAnalystsResponse, PostInterviewingResponse, PostResearchResponse, PostResearchRequest, \
    PostGenerateChaptersResponse, PostGenerateChaptersRequest
from src.infrastructure.graphs.generate_analysts.graph import GenerateAnalystsGraph
from src.infrastructure.graphs.generate_chapters.graph import GenerateChaptersGraph
from src.infrastructure.graphs.generate_chapters.schema import ChapterWithContent
from src.infrastructure.graphs.interviewing.graph import InterviewingGraph
from src.infrastructure.graphs.research.graph import ResearchGraph
from src.schemas.common import ResponseBase
from src.domains.llm_agent.app.utils import convert_md_to_docx

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

@router.post("/generate_chapters",
             response_model=PostGenerateChaptersResponse,
             status_code=status.HTTP_200_OK)
async def generate_analysts(response: Response,
                           generate_chapters_data: PostGenerateChaptersRequest):
    logging.debug(f"Request generate chapters: {generate_chapters_data}")
    graph = GenerateChaptersGraph()
    try:
        generate_chapters_response = await graph.process(generate_chapters_data)
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        generate_chapters_response = None

    if generate_chapters_response is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseBase(
            details='Ошибка'
        )
    return PostGenerateChaptersResponse(
        msg=generate_chapters_response if generate_chapters_response else None
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


@router.post("/user_endpoint", response_class=StreamingResponse,
             responses={
                 200: {
                     "content": {"application/vnd.openxmlformats-officedocument.wordprocessingml.document": {}},
                     "description": "Returns the generated DOCX file",
                 }
             }
             )
async def user_endpoint(
        response: Response,
        user_data: PostGenerateChaptersRequest):
    logging.debug(f"Request generate analysts: {user_data}")
    generate_chapters_graph = GenerateChaptersGraph()
    research_graph = ResearchGraph()

    try:
        chapters_response = await generate_chapters_graph.process(user_data)
        chapters = chapters_response.get("chapters", [])
        user_response = await research_graph.process(PostResearchRequest(
            topic=chapters_response.get("topic", ""),
            chapters=[ChapterWithContent(
                title=chapter.title,
                numbering=chapter.numbering,
                topics=chapter.topics,
                raw_content=""
            ) for chapter in chapters],
            max_num_turns=1,
        ))
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        user_response = None

    if user_response is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseBase(details='Ошибка генерации отчета')

    try:
        md_content = user_response.get("final_report", "")
        if not md_content:
            raise ValueError("Generated content is empty")

        docx_buffer = convert_md_to_docx(md_content)

        return StreamingResponse(
            content=docx_buffer,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": "attachment; filename=report.docx",
                "Content-Length": str(docx_buffer.getbuffer().nbytes)
            }
        )

    except Exception as e:
        logging.error(f"DOCX conversion error: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ResponseBase(details='Ошибка конвертации в DOCX')
