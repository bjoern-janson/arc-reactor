"""
ARC Reality Coupling Layer

Responsible for grounding adaptive decisions in external environmental
feedback.

This layer implements:

    Γ → E_t

where:

    Γ = Reality coupling strength
    E_t = Environmental evidence / invalidation signal

The reality layer determines whether the system has encountered a genuine
mismatch between its internal assumptions and external conditions.

It does not decide how to adapt. It only provides grounded evidence for
the attribution and governance layers.
"""

from .coupling import RealityCoupling
from .evidence import EnvironmentalEvidence

__all__ = [
    "RealityCoupling",
    "EnvironmentalEvidence",
]
