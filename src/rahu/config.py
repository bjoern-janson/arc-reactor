"""
RAHU Configuration.

Central configuration objects for reproducible benchmark experiments.

The configuration layer separates experimental parameters from
implementation logic, allowing systematic sweeps over:

    D_R : Regime Depth
    B_D : Dependency Breadth
    F_S : Shock Frequency

as well as agent, environment, and evaluation settings.

A RAHU experiment should be fully reconstructable from its config.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class RegimeConfig:
    """
    Environmental difficulty parameters.

    All values are normalized:

        0.0 -> minimal
        1.0 -> maximal
    """

    regime_depth: float = 0.5

    dependency_breadth: float = 0.5

    shock_frequency: float = 0.5


@dataclass(frozen=True)
class ShockConfig:
    """
    Shock suite configuration.
    """

    enabled_shocks: List[str] = field(
        default_factory=lambda: [
            "parameter_drift",
            "representation_shift",
            "rule_inversion",
            "attribution_ambiguity",
        ]
    )

    randomize_order: bool = True

    repeat_count: int = 1


@dataclass(frozen=True)
class AgentConfig:
    """
    Agent execution parameters.
    """

    agent_type: str = "arc_controller"

    learning_rate: float = 0.01

    attribution_threshold: float = 0.7

    metadata: Dict[str, object] = field(
        default_factory=dict
    )


@dataclass(frozen=True)
class EvaluationConfig:
    """
    Metrics and telemetry configuration.
    """

    track_attribution_accuracy: bool = True

    track_retention: bool = True

    track_recovery_intelligence: bool = True

    track_future_capacity: bool = True

    export_telemetry: bool = True


@dataclass(frozen=True)
class RAHUConfig:
    """
    Complete RAHU experiment configuration.

    A single object describing the entire benchmark run.
    """

    experiment_name: str = "RAHU-0"

    seed: Optional[int] = 42

    regime: RegimeConfig = field(
        default_factory=RegimeConfig
    )

    shocks: ShockConfig = field(
        default_factory=ShockConfig
    )

    agent: AgentConfig = field(
        default_factory=AgentConfig
    )

    evaluation: EvaluationConfig = field(
        default_factory=EvaluationConfig
    )

    metadata: Dict[str, object] = field(
        default_factory=dict
    )


def default_config() -> RAHUConfig:
    """
    Returns the canonical RAHU-0 configuration.
    """

    return RAHUConfig()


__all__ = [
    "RegimeConfig",
    "ShockConfig",
    "AgentConfig",
    "EvaluationConfig",
    "RAHUConfig",
    "default_config",
]
