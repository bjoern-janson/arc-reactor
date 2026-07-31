"""
ARC Permission Controller

Implements the global amplitude gate:

    λ_A =
    σ(k1(FA_c - τ_c)
      + k2(AAR* - 1)
      + k3Γ)

The permission layer answers:

    "Is structural change allowed?"

It does not decide where change occurs.
That responsibility belongs to Π_A.

ARC uses λ_A as a safety valve:

    FA_c < τ_c  →  λ_A → 0

meaning:

    insufficient attribution confidence
    → epistemic holding state
    → suppress self-modification
"""

from dataclasses import dataclass
import math


def sigmoid(x: float) -> float:
    """
    Logistic sigmoid.

    Maps arbitrary values to [0, 1].
    """

    return 1.0 / (1.0 + math.exp(-x))


def amplitude_gate(
    attribution_confidence: float,
    confidence_threshold: float,
    attribution_advantage_ratio: float,
    reality_coupling: float,
    k1: float = 1.0,
    k2: float = 1.0,
    k3: float = 1.0,
) -> float:
    """
    Calculate ARC global plasticity permission.

    Formula:

        λ_A =
        σ(
            k1(FA_c - τ_c)
          + k2(AAR* - 1)
          + k3Γ
        )

    Args:
        attribution_confidence:
            FA_c

        confidence_threshold:
            τ_c

        attribution_advantage_ratio:
            AAR*

        reality_coupling:
            Γ

    Returns:
        λ_A ∈ [0, 1]
    """

    activation = (
        k1 * (attribution_confidence - confidence_threshold)
        + k2 * (attribution_advantage_ratio - 1.0)
        + k3 * reality_coupling
    )

    return sigmoid(activation)


@dataclass
class PermissionController:
    """
    Stateful ARC permission governor.

    Stores the calibration parameters controlling
    global modification permission.
    """

    confidence_threshold: float = 0.8

    k1: float = 1.0
    k2: float = 1.0
    k3: float = 1.0

    def evaluate(
        self,
        attribution_confidence: float,
        attribution_advantage_ratio: float,
        reality_coupling: float,
    ) -> float:
        """
        Compute λ_A.

        Returns:
            Global modification permission.
        """

        return amplitude_gate(
            attribution_confidence=attribution_confidence,
            confidence_threshold=self.confidence_threshold,
            attribution_advantage_ratio=attribution_advantage_ratio,
            reality_coupling=reality_coupling,
            k1=self.k1,
            k2=self.k2,
            k3=self.k3,
        )

    def epistemic_holding(
        self,
        attribution_confidence: float,
    ) -> bool:
        """
        Determines whether ARC should freeze modification.

        Condition:

            FA_c < τ_c
        """

        return attribution_confidence < self.confidence_threshold
