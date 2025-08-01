from src.depends import get_llm_graph, get_prompt_builder
from src.infrastructure.graphs.generate_analysts.schema import GenerateAnalystsState, Perspectives
from src.infrastructure.graphs.schema import MetadataClass
from src.infrastructure.graphs.utils import llm_call
from src.configs.logger import LOGGER



async def create_analysts(state: GenerateAnalystsState) -> dict:
    """ Create analysts """
    topic = state.get("topic", "")
    chapters=state.get("chapters", [])
    num_analysts = len(chapters)
    formatted_str_chapters = "\n\n".join([f"{chapter.chapter}" for chapter in chapters])
    LOGGER.debug(f"create_analysts: {state}")
    LOGGER.debug("-------------------")

    # Enforce structured output
    structured_llm = get_llm_graph().with_structured_output(Perspectives, include_raw=True)

    # Generate question
    query = get_prompt_builder().build_generate_analysts_prompt(
        topic=topic,
        chapters=formatted_str_chapters,
        num_analysts=num_analysts
    )
    analysts = await llm_call(llm=structured_llm, prompt=query)

    metadata = MetadataClass(
        output_tokens=analysts.get("raw").usage_metadata.get("output_tokens"),
        input_tokens=analysts.get("raw").usage_metadata.get("input_tokens")
    )

    return {
        "analysts": analysts.get("parsed").analysts[:num_analysts],
        "metadata": metadata
    }
