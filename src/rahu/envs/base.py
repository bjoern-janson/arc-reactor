"""
Base environment interface for RAHU.

Every RAHU environment represents a controlled adaptive benchmark
designed to inject a specific structural invalidation (shock) into an
agent while exposing ground-truth attribution for evaluation.

Concrete environments (Parameter Shift, Representation Shift, Rule
Inversion, Attribution Ambiguity, etc.) inherit from this class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class StepResult:
    """
    Result returned after one environment step.
    """

    observation: Any
    reward: float
    terminated: bool
    truncated: bool = False

    info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ShockMetadata:
    """
    Ground-truth description of the active regime change.

    This information is intended for evaluation and oracle baselines.
    Learned ARC agents should not consume these fields directly.
    """

    shock_name: str

    failure_layer: str

    regime_depth: float

    dependency_breadth: float

    shock_frequency: float

    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseEnvironment(ABC):
    """
    Abstract RAHU environment.

    Every implementation should expose a reproducible adaptive task
    together with precise structural labels describing why the task
    changed.
    """

    def __init__(self):
        self.current_step = 0
        self.current_regime = 0
        self.current_shock: Optional[ShockMetadata] = None

    @abstractmethod
    def reset(
        self,
        seed: Optional[int] = None,
    ) -> Any:
        """
        Reset the environment.

        Returns the initial observation.
        """
        raise NotImplementedError

    @abstractmethod
    def step(
        self,
        action: Any,
    ) -> StepResult:
        """
        Advance the environment one timestep.
        """
        raise NotImplementedError

    @abstractmethod
    def inject_shock(
        self,
    ) -> ShockMetadata:
        """
        Trigger the next environmental regime change.

        Returns the ground-truth shock metadata.
        """
        raise NotImplementedError

    @abstractmethod
    def ground_truth_failure_layer(
        self,
    ) -> str:
        """
        Return the structural layer actually invalidated.

        Typical values include:

            parameter
            representation
            operator
            ontology
        """
        raise NotImplementedError

    def get_shock_metadata(
        self,
    ) -> Optional[ShockMetadata]:
        """
        Return metadata describing the currently active shock.
        """

        return self.current_shock

    def get_regime(
        self,
    ) -> int:
        """
        Return the current regime identifier.
        """

        return self.current_regime

    def get_step(
        self,
    ) -> int:
        """
        Return the current timestep.
        """

        return self.current_step
