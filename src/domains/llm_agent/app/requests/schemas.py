from typing import List, Union, Literal

from pydantic import BaseModel, field_validator

from src.chat.infrastucture.graph.schemas import OutputState
from src.chat.infrastucture.persona.schemas.memory import MemoryEntity
from src.chat.infrastucture.persona.schemas.persona import PersonaEntity
from src.chat.schemas.common import MessageHistory, ResponseBase


class PostChatRequest(BaseModel):
    request: str
    persona: PersonaEntity
    memories: List[MemoryEntity]
    messages: List[MessageHistory] = []
    language: Literal["en", "ru"] = "en"

    @field_validator("memories")
    @classmethod
    def check_memories_not_empty(cls, value: List[MemoryEntity]
                                 ) -> List[MemoryEntity]:
        if len(value) < 1:
            raise ValueError('Memories cannot be empty')
        return value

    @field_validator("language")
    @classmethod
    def check_available_language(cls, value: Literal["en", "ru"]
                                 ) -> Literal["en", "ru"]:
        if value not in ["en", "ru"]:
            raise ValueError('Language must be either "en" or "ru"')
        return value


class PostChatResponse(ResponseBase):
    msg: Union[None, OutputState]


class Scrap(BaseModel):
    html: str
