from langchain_community.document_loaders import WikipediaLoader
from langchain_core.messages import get_buffer_string, BaseMessage, AIMessage

from src.configs.logger import LOGGER
from src.depends import get_prompt_builder, get_llm_graph, get_tavily_search
from src.infrastructure.graphs.interviewing.schema import InterviewState, SearchQuery
from src.infrastructure.graphs.schema import MetadataClass
from src.infrastructure.graphs.utils import llm_call

async def generate_question(state: InterviewState):
    """ Node to generate a question """

    # Get state
    analyst = state.get("analyst")
    messages = state.get("messages")
    topic = state.get("topic")
    chapter = state.get("chapter", "")
    LOGGER.debug(f"generate_question: {state}")
    LOGGER.debug("-------------------")

    # Generate question
    system_message = get_prompt_builder().build_generate_question_prompt(
        chapter=chapter.chapter,
        person=analyst.persona,
        topic=topic
    )
    question = await llm_call(llm=get_llm_graph(), prompt=system_message+messages)

    metadata = MetadataClass(
        output_tokens=question.usage_metadata.get("output_tokens"),
        input_tokens=question.usage_metadata.get("input_tokens")
    )

    # Write messages to state
    return {
        "messages": [question],
        "metadata": metadata
    }

async def search_wikipedia(state: InterviewState):
    """ Retrieve docs from wikipedia """
    LOGGER.debug(f"search_wikipedia: {state}")
    LOGGER.debug("-------------------")
    # Search query
    structured_llm = get_llm_graph().with_structured_output(SearchQuery, include_raw=True)
    search_instructions = get_prompt_builder().build_search_instructions_prompt()
    search_query = await llm_call(llm=structured_llm, prompt=search_instructions + state.get("messages", []))

    # Extract query text
    parsed = search_query.get("parsed")
    query_text = parsed.search_query if parsed else None

    # Execute search only if query exists
    if query_text:
        try:
            search_docs = WikipediaLoader(
                query=query_text,
                load_max_docs=2
            ).load()
        except Exception as e:
            LOGGER.error(f"Wikipedia search error: {str(e)}", exc_info=True)
            search_docs = []
    else:
        search_docs = []

    # Format documents
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata.get("source", "")}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content}\n</Document>'
            for doc in search_docs
        ]
    )

    metadata = MetadataClass(
        output_tokens=search_query.get("raw").usage_metadata.get("output_tokens"),
        input_tokens=search_query.get("raw").usage_metadata.get("input_tokens")
    )

    return {
        "context": [formatted_search_docs],
        "metadata": metadata
    }

async def search_web(state: InterviewState):
    """ Retrieve docs from internet """
    LOGGER.debug(f"search_web: {state}")
    LOGGER.debug("-------------------")
    # Search query
    structured_llm = get_llm_graph().with_structured_output(SearchQuery, include_raw=True)
    search_instructions = get_prompt_builder().build_search_instructions_prompt()
    search_query = await llm_call(llm=structured_llm, prompt=search_instructions + state.get("messages", []))

    # Extract query text
    parsed = search_query.get("parsed")
    query_text = parsed.search_query if parsed else None

    # Execute search only if query exists
    if query_text:
        try:
            search_docs = get_tavily_search().invoke(query_text)
        except Exception as e:
            LOGGER.error(f"Wikipedia search error: {str(e)}", exc_info=True)
            search_docs = []
    else:
        search_docs = []

    # Format documents
    LOGGER.debug(f"search_web_documents: {search_docs}")
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc.get("url")}"/>\n{doc.get("content")}\n</Document>'
            for doc in search_docs.get("results", [])
        ]
    )

    metadata = MetadataClass(
        output_tokens=search_query.get("raw").usage_metadata.get("output_tokens"),
        input_tokens=search_query.get("raw").usage_metadata.get("input_tokens")
    )

    return {
        "context": [formatted_search_docs],
        "metadata": metadata
    }

async def generate_answer(state: InterviewState):
    """ Node to answer a question """

    # Get state
    analyst = state.get("analyst")
    topic = state.get("topic", "")
    chapter = state.get("chapter")

    messages = state.get("messages")
    context = state.get("context")
    LOGGER.debug(f"generate_answer: {state}")
    LOGGER.debug("-------------------")

    # Answer question
    system_message = get_prompt_builder().build_answer_instructions_prompt(
        person=analyst.persona,
        topic=topic,
        chapter=chapter.chapter,
        context=context,
    )
    answer = await llm_call(llm=get_llm_graph(), prompt=system_message+messages)

    # Name the message as coming from the expert
    answer.name = "expert"

    metadata = MetadataClass(
        output_tokens=answer.usage_metadata.get("output_tokens"),
        input_tokens=answer.usage_metadata.get("input_tokens")
    )

    # Append it to state
    return {
        "messages": [answer],
        "metadata": metadata,
    }
def save_interview(state: InterviewState):
    """ Save interviews """

    # Get messages
    messages = state.get("messages")

    # Convert interview to a string
    interview = get_buffer_string(messages)

    # Save to interviews key
    return {"interview": interview}

def route_messages(state: InterviewState,
                   name: str = "expert"):

    """ Route between question and answer """

    # Get messages
    messages = state.get("messages")
    max_num_turns = state.get("max_num_turns",2)

    # Check the number of expert answers
    num_responses = len(
        [m for m in messages if isinstance(m, AIMessage) and m.name == name]
    )

    # End if expert has answered more than the max turns
    if num_responses >= max_num_turns:
        return 'save_interview'

    # This router is run after each question - answer pair
    # Get the last question asked to check if it signals the end of discussion
    last_question = messages[-2]

    if "Thank you so much for your help" in last_question.content:
        return 'save_interview'
    return "ask_question"

async def write_section(state: InterviewState):
    """ Node to answer a question """

    # Get state
    topic = state.get("topic", "")
    interview = state.get("interview")
    context = state.get("context")
    analyst = state.get("analyst")
    chapter = state.get("chapter")
    LOGGER.debug(f"write_section: {state}")
    LOGGER.debug("-------------------")

    # Write section using either the gathered source docs from interview (context) or the interview itself (interview)
    prompt = get_prompt_builder().build_section_writer_instructions_prompt(
        person=analyst.persona,
        topic=topic,
        chapter=chapter.chapter,
        context=context,
        interview=interview,
    )
    section = await llm_call(llm=get_llm_graph(), prompt=prompt)

    metadata = MetadataClass(
        output_tokens=section.usage_metadata.get("output_tokens"),
        input_tokens=section.usage_metadata.get("input_tokens")
    )

    # Append it to state
    return {
        "sections": [section.content],
        "metadata": metadata,
    }
