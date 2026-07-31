"""
ARC-Full Learned Attribution Controller

The complete Arc Reactor agent.

Unlike ARC-Lite, ARC-Full does not receive ground-truth failure
labels. It must infer:

    P(L_i | E_t)

from environmental evidence, estimate confidence, determine
whether intervention is economically justified, allocate
plasticity, and execute the smallest sufficient correction.

Control pipeline:

    Γ
    ↓
    E_t
    ↓
    P(L_i | E_t)
    ↓
    FA_c
    ↓
    λ_A
    ↓
    Π_A
    ↓
    ΔS
    ↓
    RI
"""


from typing import Any, Dict

from .base import (
    ARCBaseAgent,
    AttributionOutput,
    Intervention,
)

from ..attribution.diagnosis import FailureDiagnoser
from ..attribution.confidence import ConfidenceEstimator
from ..governor.permission import PermissionGate
from ..permeability.allocation import PlasticityAllocator


class ARCController(ARCBaseAgent):
    """
    Learned ARC diagnostic controller.

    The system must discover:
        - where it failed
        - whether it knows enough
        - how much change is allowed
        - where change should occur
    """

    def __init__(
        self,
        confidence_threshold: float = 0.7,
    ):
        super().__init__()

        self.diagnoser = FailureDiagnoser()

        self.confidence_estimator = (
            ConfidenceEstimator()
        )

        self.permission_gate = (
            PermissionGate(
                threshold=confidence_threshold
            )
        )

        self.allocator = (
            PlasticityAllocator()
        )

        self.last_attribution = None
        self.last_permission = 0.0
        self.last_allocation = {}

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
        Stores environmental evidence.

        Reality coupling Γ enters here.
        """

        self.state.memory.append(
            observation
        )

    def diagnose(
        self,
    ) -> AttributionOutput:
        """
        Infer failure location.

        Learns:

            P(L_i | E_t)

        rather than receiving oracle labels.
        """

        evidence = self.state.memory

        posterior = (
            self.diagnoser.predict(
                evidence
            )
        )

        confidence = (
            self.confidence_estimator.compute(
                posterior
            )
        )

        output = AttributionOutput(
            failure_posterior=posterior,
            confidence=confidence,
            metadata={
                "diagnostic_type": "learned",
            },
        )

        self.last_attribution = output

        return output

    def decide_permission(
        self,
        aar: float = 1.0,
        reality_signal: float = 1.0,
    ) -> float:
        """
        Compute global plasticity permission.

        Implements:

            λ_A =
            σ(
              k1(FA_c-τ_c)
              +
              k2(AAR*-1)
              +
              k3Γ
            )

        The gate collapses under uncertainty,
        producing the epistemic holding state.
        """

        if self.last_attribution is None:
            return 0.0

        permission = (
            self.permission_gate.compute(
                confidence=(
                    self.last_attribution.confidence
                ),
                aar=aar,
                reality_signal=reality_signal,
            )
        )

        self.last_permission = permission

        return permission

    def allocate_plasticity(
        self,
    ) -> Dict[str, float]:
        """
        Compute spatial permeability:

            Π_A(L_i)

        using:

        - failure posterior
        - attribution confidence
        - intervention costs

        """

        if self.last_attribution is None:
            return {
                layer: 0.0
                for layer in self.layers
            }

        allocation = (
            self.allocator.allocate(
                posterior=(
                    self.last_attribution
                    .failure_posterior
                ),
                confidence=(
                    self.last_attribution
                    .confidence
                ),
            )
        )

        self.last_allocation = allocation

        return allocation

    def intervene(
        self,
        allocation: Dict[str, float],
        permission: float,
    ) -> Intervention:
        """
        Execute bounded structural correction.

        Implements:

            ΔS_i =
            λ_A Π_A(L_i) ΔS_max
        """

        if permission <= 0:
            return Intervention(
                layer="none",
                magnitude=0.0,
                metadata={
                    "state": "epistemic_holding",
                },
            )

        target_layer = max(
            allocation,
            key=allocation.get,
        )

        magnitude = (
            permission
            *
            allocation[target_layer]
        )

        return Intervention(
            layer=target_layer,
            magnitude=magnitude,
            metadata={
                "controller": "arc_full",
                "oracle": False,
                "permission": permission,
                "allocation": allocation,
            },
        )

    def evaluate(
        self,
    ) -> Dict[str, float]:
        """
        Runtime metrics populated by RAHU telemetry.

        Placeholder interface.
        """

        return {
            "AE_w": 0.0,
            "S_retained": 0.0,
            "RI": 0.0,
            "C_future": 0.0,
        }
