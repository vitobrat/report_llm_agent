from langchain_core.messages import SystemMessage, HumanMessage, AnyMessage

from src.configs.constants import PROJECT_ROOT

from pathlib import Path
import yaml
from typing import Dict


class PromptManager:
    def __init__(
            self,
            prompts_dir: Path = Path(PROJECT_ROOT, "src", "infrastructure", "prompts")
    ):
        self.prompts: Dict[str, Dict[str, str]] = {}
        self.load_prompts(prompts_dir)

    def load_prompts(self, base_path: Path):
        """Загружает все prompt.yaml файлы из поддиректорий"""
        for category_dir in base_path.iterdir():
            if not category_dir.is_dir():
                continue

            config_file = category_dir / "prompt.yaml"
            if not config_file.exists():
                continue

            with open(config_file, "r", encoding="utf-8") as f:
                category_name = category_dir.name
                self.prompts[category_name] = yaml.safe_load(f) or {}

    def get_template(self, category: str, template_name: str) -> str:
        """Возвращает шаблон из указанной категории"""
        if category in self.prompts:
            return self.prompts[category].get(template_name, "")
        return ""


class ChatPromptBuilder:
    def __init__(self, prompt_manager: PromptManager):
        self.pm = prompt_manager

    def build_generate_analysts_prompt(self,
                                       topic: str,
                                       num_analysts) -> list[AnyMessage]:
        system_generate_analysts_prompt = self.pm.get_template(
            "generate_analysts",
            "system_generate_analysts_prompt"
        )
        generate_analysts_prompt = self.pm.get_template(
            "generate_analysts",
            "generate_analysts_prompt"
        )

        return [
            SystemMessage(content=system_generate_analysts_prompt.format(
                topic=topic,
                num_analysts=num_analysts
            )),
            HumanMessage(content=generate_analysts_prompt),
        ]

    def build_generate_chapters_prompt(self,
                                       topic: str,
                                       num_chapters) -> list[AnyMessage]:
        system_generate_chapters_prompt = self.pm.get_template(
            "generate_chapters",
            "system_generate_chapters_prompt"
        )
        generate_chapters_prompt = self.pm.get_template(
            "generate_chapters",
            "generate_chapters_prompt"
        )

        return [
            SystemMessage(content=system_generate_chapters_prompt),
            HumanMessage(content=generate_chapters_prompt.format(
                topic=topic,
                num_chapters=num_chapters
            )),
        ]

    def build_generate_question_prompt(self, person: str, topic: str) -> list[AnyMessage]:
        system_generate_question_prompt = self.pm.get_template(
            "interviewing",
            "system_question_instructions",
        )

        return [
            SystemMessage(content=system_generate_question_prompt.format(
                person=person,
                topic=topic,
            ))
        ]

    def build_search_instructions_prompt(self) -> list[AnyMessage]:
        system_search_instructions_prompt = self.pm.get_template(
            "interviewing",
            "system_search_instructions",
        )

        return [
            SystemMessage(content=system_search_instructions_prompt)
        ]

    def build_answer_instructions_prompt(self, goals: str, context: list) -> list[AnyMessage]:
        system_answer_instructions_prompt = self.pm.get_template(
            "interviewing",
            "system_answer_instructions",
        )

        return [
            SystemMessage(content=system_answer_instructions_prompt.format(
                goals=goals,
                context=context,
            ))
        ]

    def build_section_writer_instructions_prompt(self,
                                                 focus: str,
                                                 interview: str,
                                                 context: list) -> list[AnyMessage]:
        system_section_writer_instructions_prompt = self.pm.get_template(
            "interviewing",
            "system_section_writer_instructions",
        )

        section_writer_instructions_prompt = self.pm.get_template(
            "interviewing",
            "section_writer_instructions",
        )

        return [
            SystemMessage(content=system_section_writer_instructions_prompt.format(
                focus=focus,
            )),
            HumanMessage(content=section_writer_instructions_prompt.format(
                context=context,
            ))
        ]

    def build_report_writer_instructions_prompt(self, topic: str, context: str) -> list[AnyMessage]:
        system_report_writer_instructions_prompt = self.pm.get_template(
            "research",
            "system_report_writer_instructions",
        )
        report_writer_instructions_prompt = self.pm.get_template(
            "research",
            "report_writer_instructions",
        )

        return [
            SystemMessage(content=system_report_writer_instructions_prompt.format(
                topic=topic,
                context=context,
            )),
            HumanMessage(content=report_writer_instructions_prompt),
        ]

    def build_intro_instructions_prompt(self, topic: str, formatted_str_sections: str) -> list[AnyMessage]:
        system_intro_instructions_prompt = self.pm.get_template(
            "research",
            "system_intro_instructions",
        )

        return [
            SystemMessage(content=system_intro_instructions_prompt.format(
                topic=topic,
                formatted_str_sections=formatted_str_sections,
            ))
        ]

    def build_conclusion_instructions_prompt(self, topic: str, formatted_str_sections: str) -> list[AnyMessage]:
        system_conclusion_instructions_prompt = self.pm.get_template(
            "research",
            "system_conclusion_instructions",
        )

        return [
            SystemMessage(content=system_conclusion_instructions_prompt.format(
                topic=topic,
                formatted_str_sections=formatted_str_sections,
            ))
        ]