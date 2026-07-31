"""
Oracle Reset Agent

The theoretical upper-bound baseline for the Arc Reactor Framework.

The Oracle Reset Agent represents an impossible idealized controller:
it has perfect knowledge of:

    P(L_i | E_t) = 1

It knows:
    - exactly what failed
    - exactly how much to change
    - exactly which structural layer requires intervention

Unlike ARC-Full, it does not need to learn attribution.
Unlike ARC-Lite, it represents the ideal limit of intervention efficiency.

Purpose in RAHU:

    RI_ARC-Full / RI_Oracle

measures how close learned ARC approaches perfect adaptive control.

This agent is not intended as a realistic architecture.
It defines the theoretical ceiling.
"""


from typing import Any, Dict

from .base import (
    ARCBaseAgent,
    AttributionOutput,
    Intervention,
)


class OracleResetAgent(ARCBaseAgent):
    """
    Perfect-information adaptive controller.

    Assumptions:

        - perfect failure attribution
        - zero diagnostic error
        - optimal intervention magnitude
        - minimal sufficient change

    This establishes the upper performance bound.
    """

    def __init__(self):
        super().__init__()

        self.layers = [
            "parameter",
            "representation",
            "operator",
            "ontology",
        ]

        self.last_failure = None

    def observe(
        self,
        observation: Any,
    ) -> None:
        """
        Receives environment state.

        Oracle has access to hidden ground truth.
        """

        self.state.memory.append(
            observation
        )

    def diagnose(
        self,
        true_failure_layer: str,
    ) -> AttributionOutput:
        """
        Perfect attribution.

        Equivalent to:

            P(L_i | E_t) = 1

        for the true failure layer.
        """

        posterior = {
            layer: (
                1.0
                if layer == true_failure_layer
                else 0.0
            )
            for layer in self.layers
        }

        output = AttributionOutput(
            failure_posterior=posterior,
            confidence=1.0,
            metadata={
                "diagnostic_type": "oracle",
            },
        )

        self.last_failure = (
            true_failure_layer
        )

        return output

    def decide_permission(
        self,
    ) -> float:
        """
        Perfect economic and epistemic confidence.

        Full permission is always justified
        when intervention is necessary.
        """

        return 1.0

    def allocate_plasticity(
        self,
    ) -> Dict[str, float]:
        """
        Perfect spatial allocation.

        All plasticity goes only to the
        minimum sufficient layer.
        """

        if self.last_failure is None:
            return {
                layer: 0.0
                for layer in self.layers
            }

        return {
            layer: (
                1.0
                if layer == self.last_failure
                else 0.0
            )
            for layer in self.layers
        }

    def intervene(
        self,
        allocation: Dict[str, float],
        permission: float,
    ) -> Intervention:
        """
        Executes minimal necessary correction.

        No wasted mutation.
        No exploratory damage.
        """

        target_layer = max(
            allocation,
            key=allocation.get,
        )

        return Intervention(
            layer=target_layer,
            magnitude=permission,
            metadata={
                "controller": "oracle_reset",
                "oracle": True,
                "optimal_intervention": True,
            },
        )

    def evaluate(
        self,
    ) -> Dict[str, float]:
        """
        Theoretical maximum metrics.
        """

        return {
            "AE_w": 1.0,
            "S_retained": 1.0,
            "RI": 1.0,
            "C_future": 1.0,
        }
