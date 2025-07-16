from src.depends import get_llm_graph, get_prompt_builder
from src.infrastructure.graphs.generate_chapters.schema import GenerateChaptersState, Chapters
from src.infrastructure.graphs.schema import MetadataClass


async def create_chapters(state: GenerateChaptersState) -> dict:
    """ Create analysts """
    topic=state.get("topic", "")
    num_chapters=state.get("num_chapters", 1)

    # Enforce structured output
    structured_llm = get_llm_graph().with_structured_output(Chapters, include_raw=True)

    # Get prompt
    prompt = get_prompt_builder().build_generate_chapters_prompt(
        topic=topic,
        num_chapters=num_chapters
    )
    chapters = await structured_llm.ainvoke(prompt)

    #Get metadata information
    metadata = MetadataClass(
        output_tokens=chapters.get("raw").usage_metadata.get("output_tokens"),
        input_tokens=chapters.get("raw").usage_metadata.get("input_tokens")
    )

    # Write the list of analysis to state
    return {
        "chapters": chapters.get("parsed").chapters,
        "metadata": metadata
    }
