import operator
from typing import Annotated

from pydantic import BaseModel

class MetadataClass(BaseModel):
    output_tokens: Annotated[int, operator.add]  # Total output tokens generated
    input_tokens: Annotated[int, operator.add]  # Total input tokens generated