from functools import lru_cache
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from src.configs.config import ProjectConfig
from src.configs.constants import PROJECT_ROOT
from src.infrastructure.prompts.prompt_manager import (
    ChatPromptBuilder,
    PromptManager
)

@lru_cache(maxsize=1)
def get_settings() -> ProjectConfig:
    return ProjectConfig.from_yaml(Path(PROJECT_ROOT, "configs", "llm_configs.yaml"))


@lru_cache(maxsize=1)
def get_prompt_builder() -> ChatPromptBuilder:
    pm = PromptManager()
    return ChatPromptBuilder(pm)


@lru_cache(maxsize=None)
def get_llm_graph(temperature=get_settings().llm.temperature,
                  top_k=get_settings().llm.top_k,
                  top_p=get_settings().llm.top_p,
                  repeat_penalty=get_settings().llm.repeat_penalty,
                  mirostat=get_settings().llm.mirostat,
                  mirostat_eta=get_settings().llm.mirostat_eta,
                  mirostat_tau=get_settings().llm.mirostat_tau,
                  num_predict=get_settings().llm.num_predict,
                  repeat_last_n=get_settings().llm.repeat_last_n,
                  num_ctx=get_settings().llm.num_ctx
                  ) -> ChatOpenAI:
    """
    Args:
        temperature: The temperature of the model.
        Increasing the temperature will make the model answer more creatively.

        top_k: How many the most possibility tokens can be use

        top_p: Works together with top-k. A higher value (e.g., 0.95) will lead
        to more diverse text, while a lower value (e.g., 0.5) will
        generate more focused and conservative text.

        repeat_penalty: Sets how strongly to penalize repetitions.
        A higher value (e.g., 1.5) will penalize repetitions more strongly,
        while a lower value (e.g., 0.9) will be more lenient.

        mirostat: Enable Mirostat sampling for controlling perplexity.
        (default: 0, 0 = disabled, 1 = Mirostat, 2 = Mirostat 2.0)

        mirostat_eta: Influences how quickly the algorithm responds to feedback
        from the generated text. A lower learning rate will result in
        slower adjustments, while a higher learning rate will make
        the algorithm more responsive.

        mirostat_tau: Controls the balance between coherence and diversity
        of the output. A lower value will result in more focused and
        coherent text.

        num_predict: How many tokens predicts during generation
        (Default: 128, -1 = infinite generation, -2 = fill context)

        repeat_last_n: Sets how far back for the model to look
        back to prevent repetition

        num_ctx: sets the size of the context window used to generate the
        next token. (Default: 2048)

    Returns:
        object: Source llm with configured params
    """
    settings = get_settings()
    llm = ChatOllama(
        base_url=settings.llm.base_llm_url,
        model=settings.llm.model_name,
    )
    llm.temperature = temperature
    llm.top_k = top_k
    llm.top_p = top_p
    llm.repeat_penalty = repeat_penalty
    llm.mirostat = mirostat
    llm.mirostat_eta = mirostat_eta
    llm.mirostat_tau = mirostat_tau
    llm.repeat_last_n = repeat_last_n
    llm.num_ctx = num_ctx
    llm.num_predict = num_predict
    return llm
