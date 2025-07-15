from langchain_community.document_loaders import WikipediaLoader
from langchain_core.messages import get_buffer_string, BaseMessage, AIMessage

from src.configs.logger import LOGGER
from src.depends import get_prompt_builder, get_llm_graph
from src.infrastructure.graphs.interviewing.schema import InterviewState, SearchQuery
from src.infrastructure.graphs.schema import MetadataClass

def get_metadata(llm_response: BaseMessage) -> MetadataClass:
    return MetadataClass(
        output_tokens=llm_response.get("raw").usage_metadata.get("output_tokens"),
        input_tokens=llm_response.get("raw").usage_metadata.get("input_tokens")
    )

def generate_question(state: InterviewState):
    """ Node to generate a question """

    # Get state
    analyst = state.get("analyst")
    messages = state.get("messages")
    topic = state.get("topic")

    # Generate question
    system_message = get_prompt_builder().build_generate_question_prompt(
        person=analyst.persona,
        topic=topic
    )
    LOGGER.debug(f"generate_question request: {system_message+messages}")
    question = get_llm_graph().invoke(system_message+messages)
    LOGGER.debug(f"generate_question response: {question}")
    LOGGER.debug("-------------------")

    metadata = MetadataClass(
        output_tokens=question.usage_metadata.get("output_tokens"),
        input_tokens=question.usage_metadata.get("input_tokens")
    )

    # Write messages to state
    return {
        "messages": [question],
        "metadata": metadata
    }

def search_wikipedia(state: InterviewState):
    """ Retrieve docs from wikipedia """
    # Search query
    structured_llm = get_llm_graph().with_structured_output(SearchQuery, include_raw=True)
    search_instructions = get_prompt_builder().build_search_instructions_prompt()
    LOGGER.debug(f"search_wikipedia request: {search_instructions + state.get("messages", [])}")
    search_query = structured_llm.invoke(search_instructions + state.get("messages", []))
    LOGGER.debug(f"search_wikipedia response: {search_query}")
    LOGGER.debug("-------------------")

    # Extract query text
    parsed = search_query.get("parsed")
    query_text = parsed.search_query if parsed else None

    # Execute search only if query exists
    if query_text:
        try:
            search_docs = WikipediaLoader(
                query=query_text,
                load_max_docs=5
            ).load()
        except Exception:
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
    LOGGER.debug(f"formatted_search_docs: {formatted_search_docs}")
    LOGGER.debug("-------------------")

    metadata = MetadataClass(
        output_tokens=search_query.get("raw").usage_metadata.get("output_tokens"),
        input_tokens=search_query.get("raw").usage_metadata.get("input_tokens")
    )

    return {
        "context": [formatted_search_docs],
        "metadata": metadata
    }

def generate_answer(state: InterviewState):
    """ Node to answer a question """

    # Get state
    analyst = state.get("analyst")
    messages = state.get("messages")
    context = state.get("context")

    # Answer question
    system_message = get_prompt_builder().build_answer_instructions_prompt(goals=analyst.persona, context=context)
    LOGGER.debug(f"generate_answer request: {system_message+messages}")
    answer = get_llm_graph().invoke(system_message+messages)
    LOGGER.debug(f"generate_answer response: {answer}")
    LOGGER.debug("-------------------")

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

def write_section(state: InterviewState):
    """ Node to answer a question """

    # Get state
    interview = state.get("interview")
    context = state.get("context")
    analyst = state.get("analyst")

    # Write section using either the gathered source docs from interview (context) or the interview itself (interview)
    prompt = get_prompt_builder().build_section_writer_instructions_prompt(
        focus=analyst.description,
        context=context,
        interview=interview, # TODO разобраться почему не используется
    )
    LOGGER.debug(f"write_section request: {prompt}")
    section = get_llm_graph().invoke(prompt)
    LOGGER.debug(f"write_section response: {section}")
    LOGGER.debug("-------------------")

    metadata = MetadataClass(
        output_tokens=section.usage_metadata.get("output_tokens"),
        input_tokens=section.usage_metadata.get("input_tokens")
    )

    # Append it to state
    return {
        "sections": [section.content],
        "metadata": metadata,
    }
