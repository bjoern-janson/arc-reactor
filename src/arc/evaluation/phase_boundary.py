"""
ARC Phase Boundary Evaluation

Tracks the predicted transition point where diagnostic control
becomes economically advantageous.

The Arc Reactor hypothesis predicts:

    AAR* < 1:
        Diagnostic overhead dominates.
        Flat optimization may outperform.

    AAR* ≈ 1:
        Critical crossover boundary.

    AAR* > 1:
        Attribution-guided correction becomes advantageous.

This module provides tools for mapping the relationship between:

    AAR*
    Regime Depth (D_R)
    Dependency Breadth (B_D)
    Shock Frequency (F_S)

and measuring whether ARC separates from baseline systems.
"""

from dataclasses import dataclass
from typing import Iterable, List, Tuple


@dataclass(frozen=True)
class PhasePoint:
    """
    Single point in the adaptive phase space.

    Attributes:

        regime_depth:
            Structural depth of environmental invalidation.

        dependency_breadth:
            Downstream impact of failure.

        shock_frequency:
            Rate of environmental perturbation.

        aar:
            Attribution Advantage Ratio.

        arc_score:
            ARC controller performance metric.

        baseline_score:
            Flat optimization performance metric.
    """

    regime_depth: float
    dependency_breadth: float
    shock_frequency: float
    aar: float
    arc_score: float
    baseline_score: float


def classify_phase(
    aar: float,
    boundary: float = 1.0,
) -> str:
    """
    Classify the adaptive regime.

    Returns:

        below_boundary:
            AAR* < 1

        crossover:
            AAR* ≈ 1

        above_boundary:
            AAR* > 1
    """

    tolerance = 0.05

    if aar < boundary - tolerance:
        return "below_boundary"

    if abs(aar - boundary) <= tolerance:
        return "crossover"

    return "above_boundary"


def find_crossover_points(
    points: Iterable[PhasePoint],
    tolerance: float = 0.05,
) -> List[PhasePoint]:
    """
    Extract points near the predicted phase transition.

    These are environments where:

        AAR* ≈ 1

    Useful for empirical testing of the ARC prediction.
    """

    return [
        point
        for point in points
        if abs(point.aar - 1.0) <= tolerance
    ]


def measure_arc_advantage(
    point: PhasePoint,
) -> float:
    """
    Compute performance separation.

    Positive:
        ARC advantage.

    Negative:
        Baseline advantage.

    Formula:

        Advantage =
            RI_ARC - RI_baseline
    """

    return point.arc_score - point.baseline_score


def detect_transition(
    points: Iterable[PhasePoint],
) -> Tuple[float | None, List[float]]:
    """
    Estimate empirical crossover.

    Searches for the first AAR value where ARC
    performance exceeds baseline.

    Returns:

        crossover AAR estimate,
        observed advantages.
    """

    ordered = sorted(
        points,
        key=lambda point: point.aar,
    )

    advantages = [
        measure_arc_advantage(point)
        for point in ordered
    ]

    for point, advantage in zip(
        ordered,
        advantages,
    ):
        if (
            point.aar >= 1.0
            and advantage > 0
        ):
            return point.aar, advantages

    return None, advantages
