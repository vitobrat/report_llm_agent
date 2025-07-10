from src.chat.domains.chat.app.requests.schemas import
from src.chat.infrastucture.graph.graph import ChatGraph, ScrapGraph
from src.chat.infrastucture.graph.schemas import


async def scrap(data: Scrap):
    scrap_graph = ScrapGraph()
    return await scrap_graph.process(data)


async def chat(data: ) -> OutputState | None:
    chat_graph = ChatGraph()

    state = InputState(
        query=data.request,
        persona=data.persona,
        memories=data.memories,
        messages=messages,
        language=data.language,
    )
    return await chat_graph.process(state)
