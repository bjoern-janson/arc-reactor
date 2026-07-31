"""
ARC Governor Module

The governor is the control layer that determines:

    - whether structural change is permitted
    - how much change is allowed
    - where permitted change is allocated

ARC separates:

    Permission:
        λ_A

    Allocation:
        Π_A

    Correction:
        ΔS

Pipeline:

    P(L_i | E_t)
            ↓
          FA_c
            ↓
          λ_A
            ↓
          Π_A
            ↓
          ΔS

The governor prevents two failure modes:

1. Rigidity:
       λ_A → 0 permanently
       System cannot adapt.

2. Runaway plasticity:
       λ_A → 1 without control
       System destroys accumulated structure.
"""

from .permission import (
    PermissionController,
    amplitude_gate,
)

from .permeability import (
    PlasticityAllocator,
    normalized_plasticity,
)

from .cost import (
    intervention_cost,
)

__all__ = [
    "PermissionController",
    "amplitude_gate",
    "PlasticityAllocator",
    "normalized_plasticity",
    "intervention_cost",
]
