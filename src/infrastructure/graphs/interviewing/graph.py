from typing import Optional
import logging

from langgraph.graph import StateGraph, START, END

from src.domains.llm_agent.app.requests.schemas import PostInterviewingRequest
from src.infrastructure.graphs.interviewing.schema import InterviewState
from src.infrastructure.graphs.interviewing.utils import generate_question, search_wikipedia, generate_answer, \
    save_interview, write_section, route_messages


class GraphError(Exception):
    """Базовый класс для ошибок в ChatGraph"""
    pass

class InterviewingGraph:
    _instance: Optional["InterviewingGraph"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InterviewingGraph, cls).__new__(cls)
            cls._instance.graph = cls._build_graph()
        return cls._instance

    @staticmethod
    def _build_graph() -> StateGraph:
        """Создаёт и компилирует граф"""
        interview_builder = StateGraph(InterviewState)
        interview_builder.add_node("ask_question", generate_question)
        # interview_builder.add_node("search_web", search_web)
        interview_builder.add_node("search_wikipedia", search_wikipedia)
        interview_builder.add_node("answer_question", generate_answer)
        interview_builder.add_node("save_interview", save_interview)
        interview_builder.add_node("write_section", write_section)

        # Flow
        interview_builder.add_edge(START, "ask_question")
        # interview_builder.add_edge("ask_question", "search_web")
        interview_builder.add_edge("ask_question", "search_wikipedia")
        # interview_builder.add_edge("search_web", "answer_question")
        interview_builder.add_edge("search_wikipedia", "answer_question")
        interview_builder.add_conditional_edges("answer_question", route_messages, ['ask_question', 'save_interview'])
        interview_builder.add_edge("save_interview", "write_section")
        interview_builder.add_edge("write_section", END)

        return interview_builder.compile().with_config(run_name="Conduct Interviews")

    async def process(self, state: PostInterviewingRequest) -> InterviewState | None:
        try:
            generate_analysts_response = await self.graph.ainvoke({
                "analyst": state.analyst,
                "max_num_turns": state.max_num_turns,
                "topic": state.topic,
            })
            return generate_analysts_response
        except Exception as e:
            logging.error(f"Error during InterviewingGraph processing: {e}")
            return None
