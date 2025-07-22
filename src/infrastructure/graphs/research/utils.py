import time
import os
from pathlib import Path

from langgraph.types import Send

from src.depends import get_prompt_builder, get_llm_graph
from src.infrastructure.graphs.research.schema import ResearchState
from src.infrastructure.graphs.schema import MetadataClass
from src.infrastructure.graphs.utils import llm_call
from src.configs.logger import LOGGER


def write_final_report(data: str):
    os.makedirs("data", exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = Path("data", f"final_report_{timestamp}.md")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

def initiate_all_interviews(state: ResearchState):
    """ This is the "map" step where we run each interview sub-graph using Send API """
    topic = state.get("topic")
    max_num_turns = state.get("max_num_turns")
    return [Send("conduct_interview", {"analyst": analyst,
                                       "max_num_turns": max_num_turns,
                                       "topic": topic,
                                       "chapter": chapter}) for analyst, chapter in zip(state.get("analysts"), state.get("chapters"))]

async def write_report(state: ResearchState):
    # Full set of sections
    sections = state.get("sections")
    topic = state.get("topic")
    chapters = state.get("chapters")
    LOGGER.debug(f"write_report: {state}")
    LOGGER.debug("-------------------")

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    formatted_str_chapters = "\n\n".join(
        [f"{chapter.chapter}" for chapter in chapters])

    # Summarize the sections into a final report
    prompt = get_prompt_builder().build_report_writer_instructions_prompt(
        topic=topic,
        chapters=formatted_str_chapters,
        formatted_str_sections=formatted_str_sections
    )
    report = await llm_call(llm=get_llm_graph(), prompt=prompt)

    metadata = MetadataClass(
        output_tokens=report.usage_metadata.get("output_tokens"),
        input_tokens=report.usage_metadata.get("input_tokens")
    )

    return {
        "content": report.content,
        "metadata": metadata,
    }
async def write_introduction(state: ResearchState):
    # Full set of sections
    sections = state.get("sections")
    topic = state.get("topic")
    LOGGER.debug(f"write_introduction: {state}")
    LOGGER.debug("-------------------")

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    # Summarize the sections into a final report

    prompt = get_prompt_builder().build_intro_instructions_prompt(
        topic=topic,
        formatted_str_sections=formatted_str_sections
    )
    intro = await llm_call(llm=get_llm_graph(), prompt=prompt)

    metadata = MetadataClass(
        output_tokens=intro.usage_metadata.get("output_tokens"),
        input_tokens=intro.usage_metadata.get("input_tokens")
    )

    return {
        "introduction": intro.content,
        "metadata": metadata,
    }

async def write_conclusion(state: ResearchState):
    # Full set of sections
    sections = state.get("sections")
    topic = state.get("topic")
    LOGGER.debug(f"write_conclusion: {state}")
    LOGGER.debug("-------------------")

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    # Summarize the sections into a final report

    prompt = get_prompt_builder().build_conclusion_instructions_prompt(
        topic=topic,
        formatted_str_sections=formatted_str_sections
    )
    conclusion = await llm_call(llm=get_llm_graph(), prompt=prompt)

    metadata = MetadataClass(
        output_tokens=conclusion.usage_metadata.get("output_tokens"),
        input_tokens=conclusion.usage_metadata.get("input_tokens"),
    )

    return {
        "conclusion": conclusion.content,
        "metadata": metadata,
    }

def finalize_report(state: ResearchState):
    """ This is the "reduce" step where we gather all the sections, combine them, and reflect on them to write the intro/conclusion """
    # Save full final report
    content = state.get("content")
    if content.startswith("## Insights"):
        content = content.strip("## Insights")
    if "## Sources" in content:
        try:
            content, sources = content.split("\n## Sources\n")
        except:
            sources = None
    else:
        sources = None

    final_report = state.get("introduction") + "\n\n---\n\n" + content + "\n\n---\n\n" + state.get("conclusion")
    if sources is not None:
        final_report += "\n\n## Sources\n" + sources
    return {"final_report": final_report}
