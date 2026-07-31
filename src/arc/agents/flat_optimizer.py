"""
Flat Optimizer Baseline

The Flat Optimizer represents traditional continual learning:

    Error → Parameter Update

It has no explicit:
    - failure attribution
    - structural diagnosis
    - permeability control
    - intervention cost model

The purpose of this agent is not to be weak, but to establish
the baseline hypothesis:

    Can raw optimization recover from regime shifts without
    knowing what part of the system failed?

RAHU expectation:

    Strong on shallow parameter drift.
    Weak on deep structural invalidation.
    Poor structural retention under repeated shocks.
"""


from typing import Any, Dict

from .base import (
    ARCBaseAgent,
    AttributionOutput,
    Intervention,
)


class FlatOptimizer(ARCBaseAgent):
    """
    Uncontrolled continual learning baseline.

    Behavioral model:

        E_t → Δθ

    All failures are treated as parameter errors.
    """

    def __init__(
        self,
        learning_rate: float = 0.01,
    ):
        super().__init__()

        self.learning_rate = learning_rate

        self.state.parameters = {
            "weights": {},
            "biases": {},
        }

        self.error_history = []

    def observe(
        self,
        observation: Any,
    ) -> None:
        """
        Store environmental feedback.

        Flat optimizer observes error magnitude only.
        """

        self.error_history.append(observation)

    def diagnose(
        self,
    ) -> AttributionOutput:
        """
        Flat optimizer has no causal attribution.

        It assumes every failure originates at
        the parameter layer.

        Equivalent posterior:

            P(parameter failure)=1
            P(all deeper layers)=0
        """

        posterior = {
            "parameter": 1.0,
            "representation": 0.0,
            "operator": 0.0,
            "ontology": 0.0,
        }

        return AttributionOutput(
            failure_posterior=posterior,
            confidence=1.0,
            metadata={
                "diagnostic_type": "fixed_parameter_assumption"
            },
        )

    def decide_permission(
        self,
    ) -> float:
        """
        Flat optimization has no amplitude governor.

        Always permits updates.
        """

        return 1.0

    def allocate_plasticity(
        self,
    ) -> Dict[str, float]:
        """
        Global parameter allocation.

        No structural localization exists.
        """

        return {
            "parameter": 1.0,
            "representation": 0.0,
            "operator": 0.0,
            "ontology": 0.0,
        }

    def intervene(
        self,
        allocation: Dict[str, float],
        permission: float,
    ) -> Intervention:
        """
        Apply unrestricted parameter update.

        Ignores:

            C(L_i)
            Π_A normalization
            λ_A gating
        """

        return Intervention(
            layer="parameter",
            magnitude=self.learning_rate,
            metadata={
                "controller": "flat_optimizer",
                "permission": permission,
                "allocation": allocation,
            },
        )

    def evaluate(
        self,
    ) -> Dict[str, float]:
        """
        Baseline telemetry.

        Flat optimizer typically achieves:
            high short-term recovery
            low structural retention
            low attribution accuracy
        """

        return {
            "AE_w": 0.0,
            "S_retained": 0.0,
            "RI": 0.0,
            "C_future": 0.0,
        }
