from typing import Union

from pydantic import BaseModel

from src.infrastructure.graphs.generate_analysts.schema import GenerateAnalystsState, Analyst
from src.infrastructure.graphs.interviewing.schema import InterviewState
from src.schemas.common import ResponseBase


class PostGenerateAnalystsRequest(BaseModel):
    topic: str
    num_analysts: int = 3

class PostGenerateAnalystsResponse(ResponseBase):
    msg: Union[None, GenerateAnalystsState]

class PostInterviewingRequest(BaseModel):
    analyst: Analyst # Analyst asking questions
    max_num_turns: int = 2 # Number turns of conversation

class PostInterviewingResponse(ResponseBase):
    msg: Union[None, InterviewState]