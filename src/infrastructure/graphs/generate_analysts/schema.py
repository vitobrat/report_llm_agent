from typing import List, Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

from src.infrastructure.graphs.schema import MetadataClass
from src.infrastructure.graphs.generate_chapters.schema import Chapter


class Analyst(BaseModel):
    affiliation: str = Field(
        description="Primary affiliation of the analyst.",
    )
    name: str = Field(
        description="Name of the analyst."
    )
    role: str = Field(
        description="Role of the analyst in the context of the topic.",
    )
    description: str = Field(
        description="Description of the analyst focus, concerns, and motives.",
    )
    @property
    def persona(self) -> str:
        return f"Name: {self.name}\nRole: {self.role}\nAffiliation: {self.affiliation}\nDescription: {self.description}\n"

class Perspectives(BaseModel):
    analysts: List[Analyst] = Field(
        description="Comprehensive list of analysts with their roles and affiliations.",
    )

class GenerateAnalystsState(TypedDict):
    topic: str # Research topic
    chapters: List[Chapter] # List of report's chapters
    analysts: List[Analyst] # Analyst asking questions
    metadata: MetadataClass  # Metadata information
