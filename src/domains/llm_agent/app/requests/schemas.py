from typing import Union, List

from pydantic import BaseModel

from src.infrastructure.graphs.generate_analysts.schema import GenerateAnalystsState, Analyst
from src.infrastructure.graphs.generate_chapters.schema import GenerateChaptersState, Chapter
from src.infrastructure.graphs.interviewing.schema import InterviewState
from src.infrastructure.graphs.research.schema import ResearchState
from src.schemas.common import ResponseBase


class PostGenerateAnalystsRequest(BaseModel):
    topic: str
    chapters: List[Chapter]

class PostGenerateAnalystsResponse(ResponseBase):
    msg: Union[None, GenerateAnalystsState]

class PostGenerateChaptersRequest(BaseModel):
    topic: str
    num_chapters: int = 3

class PostGenerateChaptersResponse(ResponseBase):
    msg: Union[None, GenerateChaptersState]

class PostInterviewingRequest(BaseModel):
    topic: str # topic of interviewing
    chapter: Chapter  # Report chapter
    analyst: Analyst # Analyst asking questions
    max_num_turns: int = 2 # Number turns of conversation

class PostInterviewingResponse(ResponseBase):
    msg: Union[None, InterviewState]


class PostResearchRequest(BaseModel):
    topic: str  # topic of interviewing
    chapters: List[Chapter]
    max_num_turns: int = 2  # Number turns of conversation of each analyst


class PostResearchResponse(ResponseBase):
    msg: Union[None, dict]