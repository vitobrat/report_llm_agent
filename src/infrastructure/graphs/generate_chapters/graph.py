import traceback
from typing import Optional
import logging

from langgraph.graph import StateGraph, START, END

from src.domains.llm_agent.app.requests.schemas import PostGenerateChaptersRequest
from src.infrastructure.graphs.generate_chapters.schema import GenerateChaptersState
from src.infrastructure.graphs.generate_chapters.utils import create_chapters
from src.depends import get_langfuse_handler


class GraphError(Exception):
    """Базовый класс для ошибок в ChatGraph"""
    pass

class GenerateChaptersGraph:
    _instance: Optional["GenerateChaptersGraph"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GenerateChaptersGraph, cls).__new__(cls)
            cls._instance.graph = cls._build_graph()
        return cls._instance

    @staticmethod
    def _build_graph() -> StateGraph:
        """Создаёт и компилирует граф"""
        builder = StateGraph(GenerateChaptersState)
        builder.add_node("create_chapters", create_chapters)

        builder.add_edge(START, "create_chapters")
        builder.add_edge("create_chapters", END)

        return builder.compile()

    async def process(self, state: PostGenerateChaptersRequest) -> GenerateChaptersState | None:
        try:
            generate_chapters_response = await self.graph.ainvoke({
                "topic": state.topic,
                "num_chapters": state.num_chapters,
            }, config={"callbacks": [get_langfuse_handler()]})
            if generate_chapters_response.get("chapters") is None:
                raise GraphError("Generated chapters list is None")
            return generate_chapters_response
        except Exception as e:
            logging.error(traceback.format_exc())
            logging.error(f"Error during GenerateChaptersGraph processing: {e}")
            return None
