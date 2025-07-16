from typing import List
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

from src.infrastructure.graphs.schema import MetadataClass


class Chapter(BaseModel):
    title: str = Field(
        description="Chapter title.",
    )
    numbering: str = Field(
        description="The numbering of this chapter is relative to all chapters."
    )
    topics: list[str] = Field(
        description="The topics that will be considered in this chapter.",
    )
    @property
    def chapter(self) -> str:
        return f"Chapter title: {self.title}\nNumbering: {self.role}\nThe topics that will be considered in this chapter: {self.topics}"

class Chapters(BaseModel):
    chapters: List[Chapter] = Field(
        description="Comprehensive list of chapters with their title, numbering and topics.",
    )

class GenerateChaptersState(TypedDict):
    topic: str # Report topic
    num_chapters: int # Number of chapters in report
    chapters: List[Chapter] # Chapters names in report
    metadata: MetadataClass  # Metadata information
