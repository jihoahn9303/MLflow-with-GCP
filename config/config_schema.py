from dataclasses import field
from typing import Any

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic.dataclasses import dataclass 

from config import model_schema


defaults = [
    "_self_",
    {"model": "logistic_regression"},
]

@dataclass
class Config:
    defaults: list[Any] = field(default_factory=lambda: defaults)
    model: model_schema.ModelConfig = MISSING
    

def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="config_schema", node=Config)
    
    model_schema._setup_config()