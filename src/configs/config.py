from pathlib import Path
from typing import Tuple, Union

import yaml
from omegaconf import OmegaConf
from pydantic import BaseModel, ConfigDict, model_validator


class _BaseValidatedConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')


class ModuleConfig(_BaseValidatedConfig):
    model_name: str

class ExperimentConfig(_BaseValidatedConfig):
    project_name: str

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