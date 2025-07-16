from typing import Union

from pydantic import BaseModel

from src.infrastructure.graphs.generate_analysts.schema import GenerateAnalystsState, Analyst
from src.infrastructure.graphs.generate_chapters.schema import GenerateChaptersState
from src.infrastructure.graphs.interviewing.schema import InterviewState
from src.infrastructure.graphs.research.schema import ResearchState
from src.schemas.common import ResponseBase


class PostGenerateAnalystsRequest(BaseModel):
    topic: str
    num_analysts: int = 3

class PostGenerateAnalystsResponse(ResponseBase):
    msg: Union[None, GenerateAnalystsState]

class PostGenerateChaptersRequest(BaseModel):
    topic: str
    num_chapters: int = 3

class PostGenerateChaptersResponse(ResponseBase):
    msg: Union[None, GenerateChaptersState]

class PostInterviewingRequest(BaseModel):
    topic: str # topic of interviewing
    analyst: Analyst # Analyst asking questions
    max_num_turns: int = 2 # Number turns of conversation

class PostInterviewingResponse(ResponseBase):
    msg: Union[None, InterviewState]


class PostResearchRequest(BaseModel):
    topic: str  # topic of interviewing
    num_analysts: int = 3
    max_num_turns: int = 2  # Number turns of conversation of each analyst


class PostResearchResponse(ResponseBase):
    msg: Union[None, dict]