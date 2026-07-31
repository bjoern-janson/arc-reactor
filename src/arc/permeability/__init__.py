"""
ARC Permeability Module

Structural permeability defines how much and where a system is
allowed to change after reality invalidates internal assumptions.

The permeability layer implements the Arc Reactor containment field:

    - prevents rigidity collapse
    - prevents uncontrolled plasticity
    - preserves structural capital

Core principle:

    Change the lowest sufficient layer.

The permeability stack operates after diagnosis and permission:

    P(L_i | E_t)
        ↓
    FA_c
        ↓
    λ_A
        ↓
    Π_A(L_i)
        ↓
    ΔS_i

Components:

    allocation:
        Spatial distribution of plasticity.

    cost:
        Structural resistance to modification.

    normalization:
        Finite plasticity budget enforcement.
"""

from .allocation import allocate_permeability
from .cost import intervention_cost
from .normalization import normalize_permeability

__all__ = [
    "allocate_permeability",
    "intervention_cost",
    "normalize_permeability",
]
