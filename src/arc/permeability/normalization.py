"""
ARC Permeability Normalization

Enforces the finite plasticity budget constraint:

    Σ Π_A(L_i) = 1

Normalization ensures that structural change remains bounded and
distributed rather than allowing simultaneous uncontrolled mutation
across the architecture.

This module represents the containment field calibration layer of
the Arc Reactor:

    Diagnosis → Permission → Allocation → Normalization → Correction
"""

from typing import Dict


def normalize_permeability(
    scores: Dict[str, float],
) -> Dict[str, float]:
    """
    Normalize raw permeability scores into a bounded allocation.

    Formula:

        Π_A(L_i) = score(L_i) / Σ score(L_j)

    Guarantees:

        Σ Π_A(L_i) = 1

    Args:

        scores:
            Unnormalized plasticity scores.

    Returns:

        Normalized permeability distribution.
    """

    if not scores:
        return {}

    total = sum(scores.values())

    if total <= 0:
        return {
            layer: 0.0
            for layer in scores
        }

    return {
        layer: value / total
        for layer, value in scores.items()
    }


def validate_budget(
    permeability: Dict[str, float],
    tolerance: float = 1e-8,
) -> bool:
    """
    Verify the finite plasticity budget constraint.

    Checks:

        Σ Π_A(L_i) ≈ 1

    or confirms that no plasticity was allocated.
    """

    if not permeability:
        return True

    total = sum(permeability.values())

    if total == 0:
        return True

    return abs(total - 1.0) <= tolerance


def apply_budget_limit(
    permeability: Dict[str, float],
    maximum_budget: float = 1.0,
) -> Dict[str, float]:
    """
    Apply a global permeability budget.

    Allows future extensions where environments may restrict
    total available plasticity.

    Default:

        maximum_budget = 1.0

    """

    if maximum_budget < 0:
        raise ValueError(
            "Maximum permeability budget cannot be negative."
        )

    total = sum(permeability.values())

    if total <= maximum_budget:
        return dict(permeability)

    scale = maximum_budget / total

    return {
        layer: value * scale
        for layer, value in permeability.items()
    }
