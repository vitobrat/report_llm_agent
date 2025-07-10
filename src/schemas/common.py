from pydantic import BaseModel
from typing import Optional, Any, Literal


class VerboseBase(BaseModel):
    id: Optional[int]


class ResponseBase(BaseModel):
    """
    ResponseBase - общая модель ответа
        msg - основные данные ответа
        detail - дополнительная информация на русском языке
    """
    msg: Any = None
    details: Optional[str] = None


class MessageHistory(BaseModel):
    type: Literal["ai", "human"]
    content: str
