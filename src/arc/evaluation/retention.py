"""
Structural retention metrics for the Arc Reactor Framework (ARC).

Measures whether an adaptive intervention preserves previously validated
capabilities while recovering from environmental invalidation.

A core ARC hypothesis is that recovery without retention is not intelligence;
it is evolutionary amnesia.
"""

from __future__ import annotations

from typing import Callable, Iterable, Sequence


def retention_score(
    pre_performance: Sequence[float],
    post_performance: Sequence[float],
    tolerance: float = 0.0,
) -> float:
    """
    Compute structural retention across previously validated tasks.

    Args:
        pre_performance:
            Performance values before adaptation.
        post_performance:
            Performance values after adaptation.
        tolerance:
            Minimum accepted performance preservation margin.

    Returns:
        Retention score in [0, 1].

    Interpretation:
        1.0 = all preserved capabilities retained.
        0.0 = complete loss of prior capability.

    Notes:
        This metric intentionally does not reward recovery on new tasks.
        It measures preservation of existing structural capital.
    """
    if len(pre_performance) != len(post_performance):
        raise ValueError(
            "Pre- and post-performance collections must have equal length."
        )

    if not pre_performance:
        return 0.0

    retained = 0

    for before, after in zip(pre_performance, post_performance):
        if after + tolerance >= before:
            retained += 1

    return retained / len(pre_performance)


def capability_retention(
    capabilities_before: Iterable[str],
    capabilities_after: Iterable[str],
) -> float:
    """
    Measure symbolic capability preservation.

    Useful for symbolic agents where capabilities can be represented
    explicitly rather than through numerical performance.

    Args:
        capabilities_before:
            Set of capabilities before intervention.
        capabilities_after:
            Set of capabilities after intervention.

    Returns:
        Fraction of original capabilities preserved.
    """
    before = set(capabilities_before)
    after = set(capabilities_after)

    if not before:
        return 0.0

    return len(before.intersection(after)) / len(before)


def evaluate_retention(
    evaluator: Callable[[], tuple[Sequence[float], Sequence[float]]],
) -> float:
    """
    Run a retention evaluation through an external evaluator.

    The evaluator should return:
        (performance_before, performance_after)

    This abstraction allows RAHU environments to plug in different
    structural retention tests.
    """
    before, after = evaluator()
    return retention_score(before, after)
