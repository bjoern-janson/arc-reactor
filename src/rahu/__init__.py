"""
RAHU: Regime-Adaptive Hierarchical Updating

The adversarial benchmark environment for the Arc Reactor Framework.

RAHU evaluates whether diagnostic control and regulated
self-modification provide adaptive advantages under regime shifts.

Core research question:

    When reality invalidates a system's assumptions,
    can it identify what must change without destroying
    what remains correct?

RAHU tests:

    - Parameter drift
    - Representation shifts
    - Rule/operator inversions
    - Attribution ambiguity

against:

    - Flat optimizers
    - Meta learners
    - ARC-Lite
    - ARC-Full
    - Oracle Reset

Evaluation focuses on:

    - Attribution Accuracy (AE_w)
    - Structural Retention (S_retained)
    - Recovery Intelligence (RI)
    - Future Capacity (C_future)
    - Phase Boundary (AAR*)
"""


__version__ = "0.1.0"


__all__ = [
    "__version__",
]
