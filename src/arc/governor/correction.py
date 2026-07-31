"""
ARC Correction Controller

Combines the two governor axes:

    λ_A  = Permission / amplitude control
    Π_A  = Spatial plasticity allocation

into the final structural intervention law:

    ΔS_i =
        λ_A · Π_A(L_i) · ΔS_max

The correction layer answers:

    "Given permission to change,
     where should the change go,
     and how much should be applied?"

ARC separates:

    Diagnosis:
        Where did reality invalidate the system?

    Governance:
        Is change allowed?

    Correction:
        Execute bounded structural modification.

This separation prevents:
    - global rewrites
    - uncontrolled plasticity
    - evolutionary amnesia
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class StructuralCorrection:
    """
    Represents an ARC structural update.

    Attributes:

        layer:
            Structural component being modified.

        magnitude:
            Amount of modification applied.
    """

    layer: str
    magnitude: float


def compute_correction(
    permission: float,
    permeability: Dict[str, float],
    max_update: float,
) -> Dict[str, StructuralCorrection]:
    """
    Compute bounded structural interventions.

    Implements:

        ΔS_i =
            λ_A · Π_A(L_i) · ΔS_max

    Args:

        permission:
            λ_A global modification permission.

        permeability:
            Π_A allocation distribution.

        max_update:
            Maximum available structural update budget.

    Returns:

        Mapping of layers to structural corrections.
    """

    if not 0 <= permission <= 1:
        raise ValueError(
            "Permission λ_A must be within [0,1]."
        )

    if max_update < 0:
        raise ValueError(
            "Maximum update must be non-negative."
        )

    if not permeability:
        raise ValueError(
            "Permeability distribution cannot be empty."
        )

    total_allocation = sum(permeability.values())

    if abs(total_allocation - 1.0) > 1e-6:
        raise ValueError(
            "Permeability distribution must sum to 1."
        )

    corrections = {}

    for layer, allocation in permeability.items():

        if allocation < 0:
            raise ValueError(
                "Permeability values must be non-negative."
            )

        corrections[layer] = StructuralCorrection(
            layer=layer,
            magnitude=(
                permission
                * allocation
                * max_update
            ),
        )

    return corrections


def total_change(
    corrections: Dict[str, StructuralCorrection],
) -> float:
    """
    Calculate total structural modification.

    Useful for verifying the global plasticity budget.
    """

    return sum(
        correction.magnitude
        for correction in corrections.values()
    )


def is_holding_state(
    permission: float,
    threshold: float = 1e-6,
) -> bool:
    """
    Detect epistemic holding.

    When:

        λ_A → 0

    the ARC reactor suppresses correction.
    """

    return permission <= threshold
