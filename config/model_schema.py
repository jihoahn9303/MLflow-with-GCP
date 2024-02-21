from typing import Optional
from omegaconf import MISSING
from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass


@dataclass
class ModelConfig:
    _target_: str = MISSING
    n_jobs: Optional[int] = None
    

@dataclass
class LogisticRegressor(ModelConfig):
    _target_: str = "sklearn.linear_model.LogisticRegression"
    penalty: Optional[str] = "l2"
    C: float = 1
    solver: str = "lbfgs"
    fit_intercept: bool = True
    max_iter: int = 150
    multi_class: str = "auto"
    warm_start: bool = False
    l1_ratio: float = 0.7
    
    
def _setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(
        group="model",
        name="logistic_regression", 
        node=LogisticRegressor
    )
    