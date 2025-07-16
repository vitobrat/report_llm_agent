import operator
from typing import List, Annotated
from typing_extensions import TypedDict

from src.infrastructure.graphs.generate_analysts.schema import Analyst
from src.infrastructure.graphs.schema import MetadataClass

def merge_metadata(first: MetadataClass, second: MetadataClass) -> MetadataClass:
    return MetadataClass(
        output_tokens=first.output_tokens + second.output_tokens,
        input_tokens=first.input_tokens + second.input_tokens
    )

class ResearchState(TypedDict):
    topic: Annotated[str, lambda first, second: first] # Research topic
    max_analysts: int # Number of analysts
    max_num_turns: Annotated[int, lambda first, second: first]  # Number turns of conversation
    analysts: List[Analyst] # Analyst asking questions
    sections: Annotated[list, operator.add] # Send() API key
    introduction: str # Introduction for the final report
    content: str # Content for the final report
    conclusion: str # Conclusion for the final report
    final_report: str # Introduction + Content + Conclusion
    metadata: Annotated[MetadataClass, merge_metadata]  # Metadata information