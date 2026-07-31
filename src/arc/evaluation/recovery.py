"""
Recovery Intelligence (RI) metric.

Implements the ARC evaluation objective:
    RI = (ΔV_post × S_retained × AE_w) / (D_s + C_adaptation)

The metric rewards systems that:
- recover viability after a shock,
- preserve validated structural capital,
- correctly attribute failures,
- minimize destructive adaptation cost.

This module intentionally does not define how agents adapt.
It only evaluates the quality of recovery.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RecoveryMetrics:
    """
    Inputs required for Recovery Intelligence calculation.

    Attributes:
        delta_viability:
            Improvement in viability after recovery.

        structural_retention:
            Fraction of validated structure preserved after adaptation.

        attribution_accuracy:
            Weighted attribution accuracy (AE_w).

        structural_damage:
            Cost of structural disruption caused by adaptation.

        adaptation_cost:
            Computational/energetic cost of recovery.
    """

    delta_viability: float
    structural_retention: float
    attribution_accuracy: float
    structural_damage: float
    adaptation_cost: float


def compute_recovery_intelligence(
    metrics: RecoveryMetrics,
    epsilon: float = 1e-12,
) -> float:
    """
    Compute Recovery Intelligence (RI).

    Formula:

        RI = (ΔV_post × S_retained × AE_w)
             --------------------------------
             D_s + C_adaptation

    Args:
        metrics:
            Recovery evaluation measurements.

        epsilon:
            Numerical stability constant preventing division by zero.

    Returns:
        Recovery Intelligence score.
    """

    numerator = (
        metrics.delta_viability
        * metrics.structural_retention
        * metrics.attribution_accuracy
    )

    denominator = (
        metrics.structural_damage
        + metrics.adaptation_cost
        + epsilon
    )

    return numerator / denominator


def classify_recovery(
    metrics: RecoveryMetrics,
    viability_threshold: float = 0.0,
    retention_threshold: float = 0.5,
    attribution_threshold: float = 0.5,
) -> str:
    """
    Classify recovery behavior.

    Categories:

    - Collapse:
        System fails to restore viability.

    - Survival Without Intelligence:
        System survives but loses structure or attribution ability.

    - ARC Adaptation:
        System restores viability while preserving and improving
        future correction capacity.
    """

    if metrics.delta_viability <= viability_threshold:
        return "collapse"

    if (
        metrics.structural_retention < retention_threshold
        or metrics.attribution_accuracy < attribution_threshold
    ):
        return "survival_without_intelligence"

    return "arc_adaptation"
