from typing import Union

from pydantic import BaseModel

from src.infrastructure.graph.schemas.generate_analysts import GenerateAnalystsState
from src.schemas.common import ResponseBase


class PostChatRequest(BaseModel):
    topic: str
    num_analysts: int = 3

class PostChatResponse(ResponseBase):
    msg: Union[None, GenerateAnalystsState]
