"""
ARC Evaluation Module

Provides measurement infrastructure for the RAHU benchmark.

The evaluation layer determines whether controlled structural
adaptation produces measurable advantages over baseline optimization.

Core metrics:

    AE_w
        Weighted Attribution Accuracy

    S_retained
        Structural retention after correction

    RI
        Recovery Intelligence

    Phase Boundary
        Detection of the AAR* crossover regime

The evaluation layer does not influence the ARC controller.
It exists as an external scientific measurement system.
"""

from .attribution_accuracy import weighted_attribution_accuracy
from .retention import structural_retention
from .recovery_intelligence import recovery_intelligence

__all__ = [
    "weighted_attribution_accuracy",
    "structural_retention",
    "recovery_intelligence",
]
