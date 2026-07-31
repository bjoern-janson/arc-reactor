"""
Arc Reactor Framework (ARC)

Adaptive Reality-Coupled Correction

Core research package for controlled self-modification,
failure attribution, structural permeability regulation,
and adaptive capacity preservation.

Architecture:

    Reality Coupling (Γ)
            ↓
    Failure Attribution P(L_i | E_t)
            ↓
    Attribution Confidence (FA_c)
            ↓
    Permission Gate (λ_A)
            ↓
    Plasticity Allocation (Π_A)
            ↓
    Structural Correction (ΔS)
            ↓
    Recovery Intelligence (RI)
            ↓
    Future Adaptive Capacity (C_future)

The ARC package contains the adaptive control mechanisms.
The RAHU package contains the adversarial evaluation environment.
"""

__version__ = "0.1.0"
__author__ = "Arc Reactor Framework Research"

from . import reality
from . import attribution
from . import governor
from . import permeability
from . import evaluation
from . import agents

__all__ = [
    "reality",
    "attribution",
    "governor",
    "permeability",
    "evaluation",
    "agents",
]
