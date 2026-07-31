"""
RAHU-0 Shock B: Representation Shift

The underlying functional rule remains valid, but the observation
encoding changes.

    Before:
        y = θx

    After:
        y = θφ(x)

The environment changes how observations are represented without
changing the causal relationship itself.

Correct attribution:
    representation

Incorrect responses:
    - parameter tuning only
    - operator rewrite
    - ontology rewrite

ARC prediction:
    Plasticity should primarily target the representation layer while
    preserving the downstream functional rule.
"""

from __future__ import annotations

from typing import Callable, Optional

import numpy as np

from .base import BaseEnvironment, ShockMetadata, StepResult


class RepresentationShiftEnvironment(BaseEnvironment):
    """
    Shock B

    Tests whether an agent can distinguish a change in observation
    encoding from deeper structural failures.
    """

    def __init__(
        self,
        theta: float = 2.0,
        shock_step: int = 100,
        x_range=(-1.0, 1.0),
        noise_std: float = 0.0,
        transform: Optional[Callable[[float], float]] = None,
    ):
        super().__init__()

        self.theta = theta
        self.shock_step = shock_step
        self.x_range = x_range
        self.noise_std = noise_std

        # Default nonlinear observation encoding.
        self.transform = transform or (lambda x: np.sign(x) * np.sqrt(abs(x)))

        self.use_transformed_representation = False

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
        self.use_transformed_representation = False

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

        encoded = (
            self.transform(x)
            if self.use_transformed_representation
            else x
        )

        target = self.theta * encoded

        reward = -abs(prediction - target)

        info = {
            "target": target,
            "encoded_value": encoded,
            "representation_shift": self.use_transformed_representation,
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
        self.use_transformed_representation = True
        self.current_regime = 1

        self.current_shock = ShockMetadata(
            shock_name="representation_shift",
            failure_layer="representation",
            regime_depth=0.4,
            dependency_breadth=0.35,
            shock_frequency=0.0,
            metadata={
                "description": (
                    "Observation encoding changes while the "
                    "underlying functional relationship is preserved."
                )
            },
        )

        return self.current_shock

    def ground_truth_failure_layer(
        self,
    ) -> str:
        return "representation"

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
