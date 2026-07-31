"""
ARC-Lite Oracle Attribution Controller

ARC-Lite represents the idealized diagnostic controller.

It receives ground-truth failure attribution directly from the
environment and therefore isolates the central question:

    If a system knows exactly what failed,
    does controlled self-modification outperform
    undifferentiated updating?

ARC-Lite removes the hardest learning problem:

    P(L_i | E_t) estimation

and tests only the governance mechanism:

    λ_A → Π_A → ΔS

RAHU role:

    Upper-bound diagnostic controller.
    Measures the maximum value of perfect attribution.
"""


from typing import Any, Dict

from .base import (
    ARCBaseAgent,
    AttributionOutput,
    Intervention,
)


class ARCLite(ARCBaseAgent):
    """
    Oracle attribution ARC controller.

    Behavioral model:

        Ground Truth Failure
              ↓
        Perfect Attribution
              ↓
        Controlled Plasticity
    """

    def __init__(
        self,
        max_intervention: float = 1.0,
    ):
        super().__init__()

        self.max_intervention = max_intervention

        self.true_failure_layer = None

        self.layers = [
            "parameter",
            "representation",
            "operator",
            "ontology",
        ]

    def observe(
        self,
        observation: Any,
    ) -> None:
        """
        Receives environment state.

        In RAHU evaluation mode, observations may contain
        oracle failure labels.
        """

        if isinstance(observation, dict):

            self.true_failure_layer = (
                observation.get(
                    "failure_layer"
                )
            )

    def diagnose(
        self,
    ) -> AttributionOutput:
        """
        Perfect attribution.

        Equivalent:

            P(L_i | E_t) = 1

        for the true failure layer.
        """

        posterior = {
            layer: (
                1.0
                if layer == self.true_failure_layer
                else 0.0
            )
            for layer in self.layers
        }

        return AttributionOutput(
            failure_posterior=posterior,
            confidence=1.0,
            metadata={
                "diagnostic_type": "oracle",
                "source": "environment_ground_truth",
            },
        )

    def decide_permission(
        self,
    ) -> float:
        """
        Perfect confidence and known economic value.

        ARC-Lite permits maximum justified change.
        """

        return 1.0

    def allocate_plasticity(
        self,
    ) -> Dict[str, float]:
        """
        Cost-weighted allocation.

        The controller changes only the failed layer.
        """

        costs = {
            "parameter": 1.0,
            "representation": 2.0,
            "operator": 5.0,
            "ontology": 10.0,
        }

        scores = {
            layer: (
                1.0 / costs[layer]
                if layer == self.true_failure_layer
                else 0.0
            )
            for layer in self.layers
        }

        total = sum(scores.values())

        if total == 0:
            return {
                layer: 0.0
                for layer in self.layers
            }

        return {
            layer: value / total
            for layer, value in scores.items()
        }

    def intervene(
        self,
        allocation: Dict[str, float],
        permission: float,
    ) -> Intervention:
        """
        Execute minimal sufficient correction.

        Implements:

            ΔS_i =
            λ_A · Π_A(L_i) · ΔS_max
        """

        target_layer = max(
            allocation,
            key=allocation.get,
        )

        magnitude = (
            permission
            *
            allocation[target_layer]
            *
            self.max_intervention
        )

        return Intervention(
            layer=target_layer,
            magnitude=magnitude,
            metadata={
                "controller": "arc_lite",
                "oracle": True,
                "allocation": allocation,
                "permission": permission,
            },
        )

    def evaluate(
        self,
    ) -> Dict[str, float]:
        """
        ARC-Lite establishes the theoretical ceiling
        for attribution-guided adaptation.
        """

        return {
            "AE_w": 1.0,
            "S_retained": 1.0,
            "RI": 1.0,
            "C_future": 1.0,
        }
