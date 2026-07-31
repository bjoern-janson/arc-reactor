"""
ARC Attribution Advantage Ratio (AAR*)

Implements the economic gate controlling whether diagnostic oversight
provides enough adaptive value to justify its computational cost.

Core question:

    Is knowing why the system failed worth the cost of knowing?

Defined as:

    AAR* =
        Expected Blast Radius Prevented
        --------------------------------
        Diagnostic Overhead + Intervention Risk

Interpretation:

    AAR* < 1:
        Diagnostic machinery costs more than the protection it provides.

    AAR* ≈ 1:
        Critical crossover boundary.

    AAR* > 1:
        Attribution-guided correction provides adaptive advantage.

The AAR module does not decide how to modify the system.
It only determines the economic justification for allowing adaptation.
"""

from dataclasses import dataclass


@dataclass
class AARComponents:
    """
    Components used to calculate AAR*.

    Attributes:
        blast_radius_prevented:
            Expected downstream damage avoided by correct attribution.

        diagnostic_overhead:
            Computational cost of maintaining attribution machinery.

        intervention_risk:
            Expected cost of making an incorrect structural change.
    """

    blast_radius_prevented: float
    diagnostic_overhead: float
    intervention_risk: float


def compute_aar(
    components: AARComponents,
) -> float:
    """
    Calculate Attribution Advantage Ratio.

    Formula:

        AAR* =
            Blast Radius Prevented
            -----------------------
            Diagnostic Overhead + Intervention Risk

    Returns:
        AAR* value.
    """

    denominator = (
        components.diagnostic_overhead
        + components.intervention_risk
    )

    if denominator <= 0:
        raise ValueError(
            "Diagnostic overhead and intervention risk "
            "must produce a positive denominator."
        )

    return (
        components.blast_radius_prevented
        / denominator
    )


def is_diagnostic_advantageous(
    aar: float,
) -> bool:
    """
    Determines whether ARC diagnosis has economic advantage.

    Condition:

        AAR* > 1
    """

    return aar > 1.0


def crossover_distance(
    aar: float,
) -> float:
    """
    Measures distance from the phase boundary.

    Positive:
        Above ARC crossover.

    Negative:
        Below crossover.

    Boundary:

        AAR* = 1
    """

    return aar - 1.0
