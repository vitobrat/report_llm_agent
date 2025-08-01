from typing import List, Annotated
from typing_extensions import TypedDict

from src.infrastructure.graphs.generate_analysts.schema import Analyst
from src.infrastructure.graphs.schema import MetadataClass
from src.infrastructure.graphs.generate_chapters.schema import ChapterWithContent
from src.infrastructure.graphs.utils import merge_metadata

class ResearchState(TypedDict):
    topic: Annotated[str, lambda first, second: second] # Research topic
    chapters: List[ChapterWithContent] # Chapters
    max_num_turns: Annotated[int, lambda first, second: second]  # Number turns of conversation
    analysts: List[Analyst] # Analyst asking questions
    introduction: str # Introduction for the final report
    content: str # Content for the final report
    conclusion: str # Conclusion for the final report
    final_report: str # Introduction + Content + Conclusion
    metadata: Annotated[MetadataClass, merge_metadata]  # Metadata information