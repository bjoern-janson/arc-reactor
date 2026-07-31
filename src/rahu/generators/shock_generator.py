"""
RAHU Shock Generator.

Centralized generator for producing reproducible environmental regime
shifts used throughout the RAHU benchmark.

The generator is intentionally independent of any particular environment.
It describes *what changes*, not *how an agent experiences it*.

The three governing ecological variables are:

    D_R : Regime Depth
    B_D : Dependency Breadth
    F_S : Shock Frequency

These parameters define the adaptive ecology under which ARC and
baseline agents are evaluated.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

import numpy as np


class ShockType(str, Enum):
    """Canonical RAHU-0 shock types."""

    PARAMETER = "parameter_drift"
    REPRESENTATION = "representation_shift"
    RULE = "rule_inversion"
    AMBIGUITY = "attribution_ambiguity"


@dataclass(frozen=True)
class Shock:
    """
    Immutable description of a regime shift.
    """

    shock_type: ShockType

    regime_depth: float

    dependency_breadth: float

    shock_frequency: float

    failure_layer: str

    metadata: Dict[str, Any] = field(default_factory=dict)


class ShockGenerator:
    """
    Generator for benchmark regime shifts.

    Produces deterministic or stochastic shock sequences while
    maintaining reproducibility through a seeded RNG.
    """

    def __init__(
        self,
        seed: Optional[int] = None,
    ):
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def parameter_drift(self) -> Shock:
        return Shock(
            shock_type=ShockType.PARAMETER,
            regime_depth=0.10,
            dependency_breadth=0.10,
            shock_frequency=0.0,
            failure_layer="parameter",
        )

    def representation_shift(self) -> Shock:
        return Shock(
            shock_type=ShockType.REPRESENTATION,
            regime_depth=0.40,
            dependency_breadth=0.35,
            shock_frequency=0.0,
            failure_layer="representation",
        )

    def rule_inversion(self) -> Shock:
        return Shock(
            shock_type=ShockType.RULE,
            regime_depth=0.75,
            dependency_breadth=0.70,
            shock_frequency=0.0,
            failure_layer="operator",
        )

    def attribution_ambiguity(self) -> Shock:
        return Shock(
            shock_type=ShockType.AMBIGUITY,
            regime_depth=0.90,
            dependency_breadth=0.85,
            shock_frequency=0.0,
            failure_layer="ambiguous",
        )

    def random_shock(self) -> Shock:
        """
        Uniform random shock from the canonical RAHU-0 suite.
        """
        choice = self.rng.choice(
            [
                self.parameter_drift,
                self.representation_shift,
                self.rule_inversion,
                self.attribution_ambiguity,
            ]
        )

        return choice()

    def sample(
        self,
        *,
        regime_depth: Optional[float] = None,
        dependency_breadth: Optional[float] = None,
        shock_frequency: Optional[float] = None,
        shock_type: Optional[ShockType] = None,
    ) -> Shock:
        """
        Generate a configurable shock.

        Any unspecified ecological variables are sampled uniformly
        over [0, 1].
        """

        if shock_type is None:
            shock_type = self.rng.choice(list(ShockType))

        builders = {
            ShockType.PARAMETER: self.parameter_drift,
            ShockType.REPRESENTATION: self.representation_shift,
            ShockType.RULE: self.rule_inversion,
            ShockType.AMBIGUITY: self.attribution_ambiguity,
        }

        shock = builders[shock_type]()

        return Shock(
            shock_type=shock.shock_type,
            failure_layer=shock.failure_layer,
            regime_depth=(
                shock.regime_depth
                if regime_depth is None
                else regime_depth
            ),
            dependency_breadth=(
                shock.dependency_breadth
                if dependency_breadth is None
                else dependency_breadth
            ),
            shock_frequency=(
                self.rng.uniform()
                if shock_frequency is None
                else shock_frequency
            ),
            metadata=shock.metadata,
        )
