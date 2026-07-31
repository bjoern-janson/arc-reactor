"""
ARC Intervention Execution

Implements the final transformation step of the permeability system:

    ΔS_i = λ_A · Π_A(L_i) · ΔS_max

This module converts governed plasticity permission and allocation
into concrete structural modification commands.

The Arc Reactor containment sequence:

    Attribution
        ↓
    Permission (λ_A)
        ↓
    Allocation (Π_A)
        ↓
    Intervention (ΔS)
        ↓
    Correction

The purpose of this layer is not to decide whether change should happen,
but to execute bounded change after governance has already been applied.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Intervention:
    """
    Represents an approved structural modification.

    Attributes:

        layer:
            Structural component receiving the update.

        magnitude:
            Amount of permitted change.

        allocation:
            Fraction of spatial plasticity budget assigned.

    """

    layer: str
    magnitude: float
    allocation: float


def compute_intervention(
    permeability: Dict[str, float],
    lambda_a: float,
    delta_s_max: float,
) -> Dict[str, Intervention]:
    """
    Compute structural interventions from governed plasticity.

    Formula:

        ΔS_i = λ_A · Π_A(L_i) · ΔS_max

    Args:

        permeability:
            Normalized spatial plasticity allocation Π_A.

        lambda_a:
            Global permission gate λ_A ∈ [0,1].

        delta_s_max:
            Maximum allowable structural change.

    Returns:

        Dictionary of layer-specific interventions.
    """

    if not 0 <= lambda_a <= 1:
        raise ValueError(
            "lambda_A must be bounded between 0 and 1."
        )

    if delta_s_max < 0:
        raise ValueError(
            "Maximum structural change cannot be negative."
        )

    interventions = {}

    for layer, allocation in permeability.items():

        magnitude = (
            lambda_a
            * allocation
            * delta_s_max
        )

        interventions[layer] = Intervention(
            layer=layer,
            magnitude=magnitude,
            allocation=allocation,
        )

    return interventions


def apply_intervention_threshold(
    interventions: Dict[str, Intervention],
    minimum_change: float = 0.0,
) -> Dict[str, Intervention]:
    """
    Remove interventions below an execution threshold.

    Prevents negligible updates from creating unnecessary
    structural churn.

    """

    return {
        layer: intervention
        for layer, intervention in interventions.items()
        if intervention.magnitude >= minimum_change
    }


def total_intervention_energy(
    interventions: Dict[str, Intervention],
) -> float:
    """
    Calculate total structural modification magnitude.

    Useful for telemetry:

        ||ΔS||

    """

    return sum(
        intervention.magnitude
        for intervention in interventions.values()
    )
