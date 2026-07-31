"""
RAHU-0 Shock D: Attribution Ambiguity

Multiple structural explanations are simultaneously plausible.

Unlike the other benchmark environments, there is intentionally no
single obvious failure layer. The correct ARC behavior is to enter an
epistemic holding state by suppressing global plasticity until further
evidence is obtained.

ARC prediction:
    High uncertainty
        ↓
    Low attribution confidence (FA_c)
        ↓
    λ_A → 0
        ↓
    Minimal intervention

This environment evaluates whether an agent knows when it should
*not* perform structural self-modification.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from .base import BaseEnvironment, ShockMetadata, StepResult


class AttributionAmbiguityEnvironment(BaseEnvironment):
    """
    Shock D

    Creates observations that are consistent with multiple competing
    structural explanations, forcing uncertainty rather than confident
    misattribution.
    """

    def __init__(
        self,
        theta: float = 2.0,
        shock_step: int = 100,
        ambiguity_probability: float = 0.5,
        x_range=(-1.0, 1.0),
        noise_std: float = 0.05,
    ):
        super().__init__()

        self.theta = theta
        self.shock_step = shock_step
        self.ambiguity_probability = ambiguity_probability
        self.x_range = x_range
        self.noise_std = noise_std

        self.ambiguity_active = False

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
        self.ambiguity_active = False

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

        if (
            self.ambiguity_active
            and self.rng.random() < self.ambiguity_probability
        ):
            # Looks like a parameter drift.
            target = 3.0 * x
            latent_cause = "parameter"
        else:
            # Looks like an operator shift.
            target = self.theta * (x ** 2)
            latent_cause = "operator"

        reward = -abs(prediction - target)

        info = {
            "target": target,
            "latent_cause": latent_cause,
            "regime": self.current_regime,
            "ambiguity": self.ambiguity_active,
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
        self.ambiguity_active = True
        self.current_regime = 1

        self.current_shock = ShockMetadata(
            shock_name="attribution_ambiguity",
            failure_layer="ambiguous",
            regime_depth=0.90,
            dependency_breadth=0.85,
            shock_frequency=0.0,
            metadata={
                "description": (
                    "Multiple structural explanations are equally "
                    "consistent with observed evidence."
                ),
                "expected_behavior": (
                    "Suppress plasticity until additional evidence "
                    "reduces attribution uncertainty."
                ),
            },
        )

        return self.current_shock

    def ground_truth_failure_layer(
        self,
    ) -> str:
        # Intentionally no unique answer.
        return "ambiguous"

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
