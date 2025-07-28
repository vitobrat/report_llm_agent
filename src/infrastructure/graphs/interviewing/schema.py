import operator
from typing import  Annotated
from langgraph.graph import MessagesState
from pydantic import BaseModel, Field

from src.infrastructure.graphs.generate_analysts.schema import Analyst
from src.infrastructure.graphs.generate_chapters.schema import Chapter
from src.infrastructure.graphs.schema import MetadataClass
from src.infrastructure.graphs.utils import merge_metadata


class InterviewState(MessagesState):
    topic: str # topic of interviewing
    max_num_turns: int # Number turns of conversation
    context: Annotated[list, operator.add] # Source docs
    chapter: Chapter
    analyst: Analyst # Analyst asking questions
    interview: str # Interview transcript
    sections: list # Final key we duplicate in outer state for Send() API
    metadata: Annotated[MetadataClass, merge_metadata]  # Metadata information

class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Search query for retrieval.")