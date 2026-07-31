"""
ARC Governor Operational States

Defines the behavioral regimes of the Arc Reactor governor.

The governor transitions between states based on:

    FA_c  = Attribution Confidence
    AAR*  = Attribution Advantage Ratio
    λ_A   = Global Permission

Operational states:

1. Stable Adaptation
   High confidence + strong economic justification.
   Targeted structural correction permitted.

2. Conservative Adaptation
   Moderate justification.
   Minimal intervention preferred.

3. Epistemic Holding
   Low confidence.
   Self-modification suppressed.

Core principle:

    Uncertainty should reduce plasticity, not increase it.
"""

from enum import Enum
from dataclasses import dataclass


class GovernorState(Enum):
    """
    ARC operating modes.
    """

    STABLE_ADAPTATION = "stable_adaptation"

    CONSERVATIVE_ADAPTATION = "conservative_adaptation"

    EPISTEMIC_HOLDING = "epistemic_holding"


@dataclass
class GovernorStateConfig:
    """
    Threshold configuration for state transitions.

    Attributes:
        confidence_threshold:
            Minimum FA_c required for intervention.

        stable_aar_threshold:
            AAR* threshold for aggressive justified adaptation.

        conservative_aar_threshold:
            Lower AAR* boundary for cautious adaptation.
    """

    confidence_threshold: float = 0.8
    stable_aar_threshold: float = 1.0
    conservative_aar_threshold: float = 0.5


def determine_state(
    attribution_confidence: float,
    attribution_advantage_ratio: float,
    config: GovernorStateConfig | None = None,
) -> GovernorState:
    """
    Determine current ARC governor state.

    Decision hierarchy:

        FA_c < τ_c
            → Epistemic Holding

        FA_c >= τ_c and AAR* > 1
            → Stable Adaptation

        Otherwise
            → Conservative Adaptation

    Args:
        attribution_confidence:
            FA_c

        attribution_advantage_ratio:
            AAR*

    Returns:
        Current governor state.
    """

    if config is None:
        config = GovernorStateConfig()

    if attribution_confidence < config.confidence_threshold:
        return GovernorState.EPISTEMIC_HOLDING

    if attribution_advantage_ratio >= config.stable_aar_threshold:
        return GovernorState.STABLE_ADAPTATION

    return GovernorState.CONSERVATIVE_ADAPTATION


def permission_multiplier(
    state: GovernorState,
) -> float:
    """
    Provides a qualitative permission scaling.

    This does not replace λ_A.
    It provides an operational prior.

    Stable:
        full permission

    Conservative:
        reduced permission

    Holding:
        zero permission
    """

    if state == GovernorState.STABLE_ADAPTATION:
        return 1.0

    if state == GovernorState.CONSERVATIVE_ADAPTATION:
        return 0.25

    if state == GovernorState.EPISTEMIC_HOLDING:
        return 0.0

    raise ValueError(
        f"Unknown governor state: {state}"
    )
