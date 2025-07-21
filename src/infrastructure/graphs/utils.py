from src.depends import get_langfuse_handler

async def llm_call(llm, prompt, **kwargs):
    return await llm.ainvoke(prompt, **kwargs)