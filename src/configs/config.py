from pathlib import Path

import yaml
from omegaconf import OmegaConf
from pydantic import BaseModel, ConfigDict, model_validator


class _BaseValidatedConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')


class LLMConfig(_BaseValidatedConfig):
    base_llm_url: str
    model_name: str
    temperature: float
    top_k: float
    top_p: float
    repeat_penalty: float
    mirostat: int
    mirostat_eta: float
    mirostat_tau: float
    num_predict: float
    repeat_last_n: int
    num_ctx: int

class ProjectConfig(_BaseValidatedConfig):
    project_name: str
    port: int
    log_level: str
    workers_number: int
    llm: LLMConfig

    @classmethod
    def from_yaml(cls, path: Path | str) -> 'ExperimentConfig':
        config = OmegaConf.to_container(OmegaConf.load(path), resolve=True)
        return cls(**config)

    def to_yaml(self, path: Path) -> None:
        with open(path, 'w') as output_file:
            yaml.safe_dump(
                self.model_dump(),
                output_file,
                default_flow_style=False,
                sort_keys=False,
            )
