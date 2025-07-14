from src.infrastructure.graph.schemas.generate_analysts import GenerateAnalystsState, Perspectives
from src.depends import get_llm_graph, get_prompt_builder
from src.infrastructure.graph.schemas.common import MetadataClass
from src.configs.logger import LOGGER


async def create_analysts(state: GenerateAnalystsState) -> dict:
    """ Create analysts """
    topic=state.get("topic", "")
    num_analysts=state.get("num_analysts", 1)

    # Enforce structured output
    structured_llm = get_llm_graph().with_structured_output(Perspectives, include_raw=True)

    # Generate question
    query = get_prompt_builder().build_generate_analysts_prompt(
        topic=topic,
        num_analysts=num_analysts
    )
    LOGGER.debug(f"Generate analysts LLM request: {query}")
    analysts = await structured_llm.ainvoke(query)
    LOGGER.debug(f"Generate analysts LLM response: {analysts}")

    #Get metadata information
    metadata = MetadataClass(
        output_tokens=analysts.get("raw").usage_metadata.get("output_tokens"),
        input_tokens=analysts.get("raw").usage_metadata.get("input_tokens")
    )

    # Write the list of analysis to state
    return {
        "analysts": analysts.get("parsed").analysts,
        "metadata": metadata
    }
