from typing import Optional
import logging

from langgraph.graph import StateGraph, START, END

from src.domains.llm_agent.app.requests.schemas import PostGenerateAnalystsRequest
from src.infrastructure.graphs.generate_analysts.schema import GenerateAnalystsState
from src.infrastructure.graphs.generate_analysts.utils import create_analysts


class GraphError(Exception):
    """Базовый класс для ошибок в ChatGraph"""
    pass

class GenerateAnalystsGraph:
    _instance: Optional["GenerateAnalystsGraph"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GenerateAnalystsGraph, cls).__new__(cls)
            cls._instance.graph = cls._build_graph()
        return cls._instance

    @staticmethod
    def _build_graph() -> StateGraph:
        """Создаёт и компилирует граф"""
        builder = StateGraph(GenerateAnalystsState)
        builder.add_node("create_analysts", create_analysts)

        builder.add_edge(START, "create_analysts")
        builder.add_edge("create_analysts", END)

        return builder.compile()

    async def process(self, state: PostGenerateAnalystsRequest) -> GenerateAnalystsState | None:
        try:
            generate_analysts_response = await self.graph.ainvoke({
                "topic": state.topic,
                "chapters": state.chapters,
            })
            if generate_analysts_response.get("analysts") is None:
                raise GraphError("Generated analysts list is None")
            return generate_analysts_response
        except Exception as e:
            logging.error(f"Error during GenerateAnalystsGraph processing: {e}")
            return None
