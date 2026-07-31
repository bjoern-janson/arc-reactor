"""
RAHU Environment Package

Environment implementations for the Regime-Adaptive Hierarchical
Updating (RAHU) benchmark.

RAHU environments are intentionally minimal, controlled test chambers
designed to isolate adaptive behavior under regime change. Each
environment exposes a well-defined structural invalidation while
providing ground-truth attribution labels for evaluation.

Current benchmark shocks:

    Shock A
        Parameter Drift
        y = 2x  →  y = 3x

    Shock B
        Representation Shift
        x → φ(x)

    Shock C
        Rule / Operator Inversion
        y = θx → y = θx²

    Shock D
        Attribution Ambiguity
        Multiple plausible failure layers.

Every environment should expose:

    - observations
    - rewards / losses
    - regime metadata
    - ground-truth failure layer
    - shock metadata

These environments serve as the empirical foundation for testing
the ARC hypothesis:

    Does attribution-guided, regulated plasticity outperform
    undifferentiated optimization under deep regime shifts?
"""

from .base import BaseEnvironment
from .parameter_shift import ParameterShiftEnvironment
from .representation_shift import RepresentationShiftEnvironment
from .rule_inversion import RuleInversionEnvironment
from .attribution_ambiguity import AttributionAmbiguityEnvironment

__all__ = [
    "BaseEnvironment",
    "ParameterShiftEnvironment",
    "RepresentationShiftEnvironment",
    "RuleInversionEnvironment",
    "AttributionAmbiguityEnvironment",
]
