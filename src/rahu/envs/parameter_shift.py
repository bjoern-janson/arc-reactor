"""
RAHU-0 Shock A: Parameter Drift

The simplest adaptive benchmark.

The underlying functional rule remains unchanged while only the
calibration parameter changes.

    Before:
        y = 2x

    After:
        y = 3x

Correct attribution:
    parameter

Incorrect responses:
    - representation rewrite
    - operator rewrite
    - ontology rewrite

ARC prediction:
    Only parameter-level plasticity should be allocated.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from .base import (
    BaseEnvironment,
    ShockMetadata,
    StepResult,
)


class ParameterShiftEnvironment(BaseEnvironment):
    """
    Shock A

    Tests whether an agent can distinguish simple parameter drift from
    deeper structural failures.
    """

    def __init__(
        self,
        parameter_before: float = 2.0,
        parameter_after: float = 3.0,
        shock_step: int = 100,
        x_range=(-1.0, 1.0),
        noise_std: float = 0.0,
    ):
        super().__init__()

        self.parameter_before = parameter_before
        self.parameter_after = parameter_after

        self.current_parameter = parameter_before

        self.shock_step = shock_step

        self.x_range = x_range
        self.noise_std = noise_std

        self.rng = np.random.default_rng()

    def reset(
        self,
        seed: Optional[int] = None,
    ) -> np.ndarray:
        if seed is not None:
            self.rng = np.random.default_rng(seed)

        self.current_step = 0
        self.current_regime = 0
        self.current_parameter = self.parameter_before
        self.current_shock = None

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
        target = self.current_parameter * x

        reward = -abs(prediction - target)

        info = {
            "target": target,
            "parameter": self.current_parameter,
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
        self.current_parameter = self.parameter_after
        self.current_regime = 1

        self.current_shock = ShockMetadata(
            shock_name="parameter_drift",
            failure_layer="parameter",
            regime_depth=0.1,
            dependency_breadth=0.1,
            shock_frequency=0.0,
            metadata={
                "before": self.parameter_before,
                "after": self.parameter_after,
            },
        )

        return self.current_shock

    def ground_truth_failure_layer(
        self,
    ) -> str:
        return "parameter"

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
