from pathlib import Path
import yaml
from typing import Dict

from langchain_core.messages import SystemMessage, HumanMessage, AnyMessage


class PromptManager:
    def __init__(
            self,
            prompts_dir: Path = Path(
                "src", "llm_agent", "infrastucture", "prompts"),
    ):
        self.prompts: Dict[str, Dict[str, str]] = {}
        self.load_prompts(Path(prompts_dir))

    def load_prompts(self, base_path: Path):
        for config_file in base_path.glob("**/*.yaml"):
            category = config_file.parent.name
            with open(config_file, "r") as f:
                self.prompts.setdefault(category, {}).update(yaml.safe_load(f))

    def get_template(self, category: str, template_name: str) -> str:
        return self.prompts.get(category, {}).get(template_name, "")


class ChatPromptBuilder:
    def __init__(self, prompt_manager: PromptManager):
        self.pm = prompt_manager

    def build_rewrite_query_tool_prompt(self,
                                        query: str) -> list[AnyMessage]:
        system_rewrite_query_tool_prompt = self.pm.get_template(
            "system",
            "rewrite_query_tool"
        )
        rewrite_query_tool_prompt = self.pm.get_template(
            "templates",
            "rewrite_query_tool"
        )

        return [
            SystemMessage(content=system_rewrite_query_tool_prompt),
            HumanMessage(content=rewrite_query_tool_prompt.format(query=query)),
        ]
