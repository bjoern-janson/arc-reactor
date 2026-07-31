"""
ARC Attribution Confidence

Implements the confidence gate:

    FA_c = max_i P(L_i | E_t)

The confidence layer measures how certain the attribution system is about
the suspected failure location.

This value does not determine whether a failure exists.
It determines whether the system has enough epistemic certainty to permit
structural intervention.

Used downstream by:

    FA_c → λ_A

where low confidence suppresses self-modification.
"""

from typing import Dict

from .diagnosis import FailureLayer, FailurePosterior


def attribution_confidence(
    posterior: FailurePosterior | Dict[FailureLayer, float],
) -> float:
    """
    Calculate attribution confidence.

    Formula:

        FA_c = max_i P(L_i | E_t)

    Args:
        posterior:
            Failure posterior distribution.

    Returns:
        Confidence value in range [0, 1].
    """

    if isinstance(posterior, FailurePosterior):
        return posterior.confidence()

    if not posterior:
        return 0.0

    return max(posterior.values())


def confidence_threshold_met(
    confidence: float,
    threshold: float,
) -> bool:
    """
    Determines whether attribution confidence is sufficient
    to permit downstream intervention.

    Args:
        confidence:
            FA_c value.

        threshold:
            Minimum required confidence τ_c.

    Returns:
        True if confidence exceeds threshold.
    """

    return confidence >= threshold


def epistemic_holding_state(
    confidence: float,
    threshold: float,
) -> bool:
    """
    Determines whether ARC should enter the epistemic holding state.

    Condition:

        FA_c < τ_c

    Meaning:
        The system should reduce permeability and avoid blind mutation.
    """

    return confidence < threshold
