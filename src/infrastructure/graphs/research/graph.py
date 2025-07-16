from typing import Optional
import logging

from langgraph.graph import StateGraph, START, END

from src.configs.logger import LOGGER
from src.domains.llm_agent.app.requests.schemas import PostResearchRequest
from src.infrastructure.graphs.generate_analysts.utils import create_analysts
from src.infrastructure.graphs.interviewing.graph import InterviewingGraph
from src.infrastructure.graphs.interviewing.schema import InterviewState
from src.infrastructure.graphs.research.schema import ResearchState
from src.infrastructure.graphs.research.utils import write_report, write_introduction, write_conclusion, \
    finalize_report, initiate_all_interviews


class GraphError(Exception):
    """Базовый класс для ошибок в ChatGraph"""
    pass

class ResearchGraph:
    _instance: Optional["ResearchGraph"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResearchGraph, cls).__new__(cls)
            cls._instance.graph = cls._build_graph()
        return cls._instance

    @staticmethod
    def _build_graph() -> StateGraph:
        """Создаёт и компилирует граф"""
        interview_builder = InterviewingGraph()
        builder = StateGraph(ResearchState)
        builder.add_node("create_analysts", create_analysts)
        builder.add_node("conduct_interview", interview_builder.graph)
        builder.add_node("write_report", write_report)
        builder.add_node("write_introduction", write_introduction)
        builder.add_node("write_conclusion", write_conclusion)
        builder.add_node("finalize_report", finalize_report)

        # Logic
        builder.add_edge(START, "create_analysts")
        builder.add_conditional_edges("create_analysts", initiate_all_interviews, ["conduct_interview"])
        builder.add_edge("conduct_interview", "write_report")
        builder.add_edge("conduct_interview", "write_introduction")
        builder.add_edge("conduct_interview", "write_conclusion")
        builder.add_edge(["write_conclusion", "write_report", "write_introduction"], "finalize_report")
        builder.add_edge("finalize_report", END)
        return builder.compile()

    async def process(self, state: PostResearchRequest) -> ResearchState | None:
        try:
            research_response = await self.graph.ainvoke({
                "topic": state.topic,
                "max_num_turns": state.max_num_turns,
                "num_analysts": state.num_analysts,
            })
            LOGGER.debug(f"research_response: {research_response}")
            return research_response
        except Exception as e:
            logging.error(f"Error during ResearchGraph processing: {e}")
            return None
