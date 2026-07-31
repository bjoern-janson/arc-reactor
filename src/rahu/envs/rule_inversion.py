"""
RAHU-0 Shock C: Rule Inversion

The representation remains unchanged while the underlying functional
rule changes.

    Before:
        y = θx

    After:
        y = θx²

The observation space is identical. The calibration parameter remains
valid. Only the governing rule/operator changes.

Correct attribution:
    operator

Incorrect responses:
    - endless parameter tuning
    - representation rewrites
    - ontology rewrites

ARC prediction:
    Plasticity should target the operator/grammar layer while
    preserving both parameter calibration and representation.
"""

from __future__ import annotations

from typing import Callable, Optional

import numpy as np

from .base import BaseEnvironment, ShockMetadata, StepResult


class RuleInversionEnvironment(BaseEnvironment):
    """
    Shock C

    Tests whether an agent can recognize that the governing rule
    has changed rather than merely its parameters.
    """

    def __init__(
        self,
        theta: float = 2.0,
        shock_step: int = 100,
        x_range=(-1.0, 1.0),
        noise_std: float = 0.0,
    ):
        super().__init__()

        self.theta = theta
        self.shock_step = shock_step
        self.x_range = x_range
        self.noise_std = noise_std

        self.rule: Callable[[float], float] = lambda x: x

        self.rng = np.random.default_rng()

    def reset(
        self,
        seed: Optional[int] = None,
    ) -> np.ndarray:
        if seed is not None:
            self.rng = np.random.default_rng(seed)

        self.current_step = 0
        self.current_regime = 0
        self.current_shock = None

        self.rule = lambda x: x

        return self._sample_observation()

    def step(
        self,
        prediction: float,
    ) -> StepResult:
        if (
            self.current_step == self.shock_step
            and self.current_regime == 0
        ):
            self.inject_shock()

        observation = self._sample_observation()

        x = float(observation[0])

        target = self.theta * self.rule(x)

        reward = -abs(prediction - target)

        info = {
            "target": target,
            "theta": self.theta,
            "regime": self.current_regime,
        }

        if self.current_shock is not None:
            info["shock"] = self.current_shock

        self.current_step += 1

        return StepResult(
            observation=observation,
            reward=reward,
            terminated=False,
            truncated=False,
            info=info,
        )

    def inject_shock(
        self,
    ) -> ShockMetadata:
        self.rule = lambda x: x**2
        self.current_regime = 1

        self.current_shock = ShockMetadata(
            shock_name="rule_inversion",
            failure_layer="operator",
            regime_depth=0.75,
            dependency_breadth=0.70,
            shock_frequency=0.0,
            metadata={
                "rule_before": "y = θx",
                "rule_after": "y = θx²",
            },
        )

        return self.current_shock

    def ground_truth_failure_layer(
        self,
    ) -> str:
        return "operator"

    def _sample_observation(
        self,
    ) -> np.ndarray:
        x = self.rng.uniform(
            self.x_range[0],
            self.x_range[1],
        )

        if self.noise_std > 0:
            x += self.rng.normal(
                0.0,
                self.noise_std,
            )

        return np.asarray([x], dtype=float)
