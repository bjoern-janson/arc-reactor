"""
ARC Future Capacity Invariant

Implements the long-horizon objective of the Arc Reactor Framework.

The governor is not optimized merely for immediate recovery.
It must preserve or expand the system's future ability to recover
from unknown future shocks.

Core invariant:

    C_future(t+1) >= C_future(t)

A successful adaptation increases or preserves adaptive optionality.

A failure occurs when:
    - short-term viability increases,
    - but future corrective capacity decreases.

This detects evolutionary amnesia:
    survival purchased by destroying the ability to adapt later.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class FutureCapacityState:
    """
    Represents adaptive capacity at a point in time.

    Attributes:

        retained_structure:
            Preserved validated internal capabilities.

        available_actions:
            Number/diversity of viable future adaptation paths.

        correction_accuracy:
            Ability to correctly diagnose future failures.

        exploration_capacity:
            Remaining ability to discover new solutions.
    """

    retained_structure: float
    available_actions: float
    correction_accuracy: float
    exploration_capacity: float


def compute_future_capacity(
    state: FutureCapacityState,
    weights: tuple[float, float, float, float] = (
        0.25,
        0.25,
        0.25,
        0.25,
    ),
) -> float:
    """
    Compute C_future.

    Composite invariant representing future adaptive optionality.

    Formula:

        C_future =
            w1*S_retained
          + w2*A_available
          + w3*AE_future
          + w4*Exploration

    All components are expected to be normalized to [0,1].
    """

    components = (
        state.retained_structure,
        state.available_actions,
        state.correction_accuracy,
        state.exploration_capacity,
    )

    if any(
        value < 0 or value > 1
        for value in components
    ):
        raise ValueError(
            "Future capacity components must be within [0,1]."
        )

    if len(weights) != 4:
        raise ValueError(
            "Future capacity requires four weights."
        )

    if abs(sum(weights) - 1.0) > 1e-6:
        raise ValueError(
            "Future capacity weights must sum to 1."
        )

    return sum(
        value * weight
        for value, weight in zip(components, weights)
    )


def future_capacity_invariant(
    current_capacity: float,
    next_capacity: float,
    tolerance: float = 0.0,
) -> bool:
    """
    Test ARC's governing invariant:

        C_future(t+1) >= C_future(t)

    Returns:

        True:
            Adaptation preserved future capacity.

        False:
            Adaptation caused adaptive degradation.
    """

    return next_capacity + tolerance >= current_capacity


def capacity_delta(
    current_capacity: float,
    next_capacity: float,
) -> float:
    """
    Measure change in future adaptive capacity.

    Positive:
        Expansion of adaptive optionality.

    Zero:
        Preservation.

    Negative:
        Evolutionary amnesia.
    """

    return next_capacity - current_capacity
