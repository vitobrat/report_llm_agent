import traceback
from typing import Optional
import logging

from langgraph.graph import StateGraph, START, END

from src.chat.domains.chat.app.requests.schemas import Scrap
from src.chat.infrastucture.graph.schemas import (
    InputState, OutputState, ChatGraphError, ScrapResponse
)
from src.chat.infrastucture.graph.utils import (
    calling_llm_chat, calling_retriever, parse_messages, scrap, translator,
    is_rewrite_query, rewrite_query_tool, route_decision, route_language
)


class ChatGraph:
    _instance: Optional["ChatGraph"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatGraph, cls).__new__(cls)
            cls._instance.graph = cls._build_graph()
        return cls._instance

    @staticmethod
    def _build_graph() -> StateGraph:
        """Создаёт и компилирует граф"""


        return builder.compile()

    async def process(self, state: InputState) -> OutputState | None:
        try:
            messages = await self.graph.ainvoke(state)
            if messages is None:
                raise ChatGraphError("Chat response is None")
            return messages
        except Exception as e:
            logging.error(f"Error during ChatGraph processing: {e}")
            return None
