"""
RAHU Regime Generator.

Generates controlled adaptive ecologies by manipulating the three
independent environmental variables proposed by the Arc Reactor
Framework:

    D_R : Regime Depth
    B_D : Dependency Breadth
    F_S : Shock Frequency

Unlike the ShockGenerator, which specifies *what* breaks, the
RegimeGenerator specifies *the ecology in which failures occur*.

This separation allows the same shock type to be evaluated under
different adaptive pressures.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

import numpy as np


@dataclass(frozen=True)
class Regime:
    """
    Description of an adaptive environment.

    Parameters
    ----------
    regime_depth
        Structural depth at which failures occur.
        0.0 -> parameter calibration
        1.0 -> ontology / architecture

    dependency_breadth
        Fraction of downstream components affected by failure.

    shock_frequency
        Probability (or normalized rate) of regime changes.
    """

    regime_depth: float
    dependency_breadth: float
    shock_frequency: float

    metadata: Dict[str, object] = field(default_factory=dict)


class RegimeGenerator:
    """
    Generator for adaptive ecologies.

    Produces controlled values for the three environmental variables
    used throughout the RAHU benchmark.

    D_R
        Regime depth.

    B_D
        Dependency breadth.

    F_S
        Shock frequency.
    """

    def __init__(
        self,
        seed: Optional[int] = None,
    ):
        self.rng = np.random.default_rng(seed)

    @staticmethod
    def _clip(value: float) -> float:
        """Clamp values into the normalized regime interval."""
        return float(np.clip(value, 0.0, 1.0))

    def create(
        self,
        *,
        regime_depth: float,
        dependency_breadth: float,
        shock_frequency: float,
        **metadata,
    ) -> Regime:
        """
        Create a deterministic regime.
        """

        return Regime(
            regime_depth=self._clip(regime_depth),
            dependency_breadth=self._clip(dependency_breadth),
            shock_frequency=self._clip(shock_frequency),
            metadata=dict(metadata),
        )

    def random(self) -> Regime:
        """
        Sample a completely random ecology.
        """

        return Regime(
            regime_depth=float(self.rng.uniform()),
            dependency_breadth=float(self.rng.uniform()),
            shock_frequency=float(self.rng.uniform()),
        )

    def shallow(self) -> Regime:
        """
        Low-depth adaptive ecology.

        Prediction:
            Flat continual learning should perform well.
        """

        return Regime(
            regime_depth=0.10,
            dependency_breadth=0.15,
            shock_frequency=0.80,
            metadata={
                "expected_winner": "flat_optimizer",
            },
        )

    def transitional(self) -> Regime:
        """
        Near the predicted ARC phase boundary.
        """

        return Regime(
            regime_depth=0.50,
            dependency_breadth=0.50,
            shock_frequency=0.50,
            metadata={
                "expected_region": "AAR≈1",
            },
        )

    def deep(self) -> Regime:
        """
        High-depth ecology.

        Prediction:
            ARC should outperform flat optimization if the
            hypothesis is correct.
        """

        return Regime(
            regime_depth=0.90,
            dependency_breadth=0.90,
            shock_frequency=0.20,
            metadata={
                "expected_winner": "arc",
            },
        )

    def interpolate(
        self,
        start: Regime,
        end: Regime,
        alpha: float,
    ) -> Regime:
        """
        Linearly interpolate between two regimes.

        Useful for sweeping across the predicted AAR* crossover.
        """

        alpha = self._clip(alpha)

        return Regime(
            regime_depth=(
                (1 - alpha) * start.regime_depth
                + alpha * end.regime_depth
            ),
            dependency_breadth=(
                (1 - alpha) * start.dependency_breadth
                + alpha * end.dependency_breadth
            ),
            shock_frequency=(
                (1 - alpha) * start.shock_frequency
                + alpha * end.shock_frequency
            ),
            metadata={
                "interpolation_alpha": alpha,
            },
        )
