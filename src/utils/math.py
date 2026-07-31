"""
Mathematical Utilities.

Shared numerical helpers used across ARC and RAHU.

Provides stable implementations for common operations:

    - normalization
    - softmax distributions
    - sigmoid gating
    - weighted averages
    - bounded scaling
    - distance calculations

This module contains generic mathematics only.
No ARC-specific interpretation belongs here.
"""

from __future__ import annotations

import math
from typing import Dict, Iterable, Sequence


def sigmoid(
    x: float,
) -> float:
    """
    Numerically stable logistic sigmoid.

    Used by higher-level controllers for bounded
    continuous gating.
    """

    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)

    z = math.exp(x)
    return z / (1.0 + z)


def softmax(
    values: Sequence[float],
    temperature: float = 1.0,
) -> list[float]:
    """
    Compute normalized softmax distribution.

    Parameters
    ----------
    values:
        Input scores.

    temperature:
        Controls distribution sharpness.
    """

    if temperature <= 0:
        raise ValueError(
            "Temperature must be positive."
        )

    scaled = [
        value / temperature
        for value in values
    ]

    maximum = max(scaled)

    exponentials = [
        math.exp(value - maximum)
        for value in scaled
    ]

    total = sum(exponentials)

    return [
        value / total
        for value in exponentials
    ]


def normalize(
    values: Sequence[float],
) -> list[float]:
    """
    Normalize values into a probability-like
    distribution.

    Ensures:

        sum(output) = 1
    """

    total = sum(values)

    if total == 0:
        raise ValueError(
            "Cannot normalize zero vector."
        )

    return [
        value / total
        for value in values
    ]


def normalize_dict(
    values: Dict[str, float],
) -> Dict[str, float]:
    """
    Normalize dictionary values while
    preserving keys.
    """

    total = sum(values.values())

    if total == 0:
        raise ValueError(
            "Cannot normalize zero dictionary."
        )

    return {
        key: value / total
        for key, value in values.items()
    }


def weighted_average(
    values: Iterable[float],
    weights: Iterable[float],
) -> float:
    """
    Compute weighted mean.
    """

    values = list(values)
    weights = list(weights)

    if len(values) != len(weights):
        raise ValueError(
            "Values and weights must match length."
        )

    denominator = sum(weights)

    if denominator == 0:
        raise ValueError(
            "Weight sum cannot be zero."
        )

    return sum(
        value * weight
        for value, weight in zip(
            values,
            weights,
        )
    ) / denominator


def clamp(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    """
    Bound value within interval.
    """

    if minimum > maximum:
        raise ValueError(
            "Minimum cannot exceed maximum."
        )

    return max(
        minimum,
        min(
            value,
            maximum,
        ),
    )


def l1_distance(
    a: Sequence[float],
    b: Sequence[float],
) -> float:
    """
    Compute Manhattan distance.
    """

    if len(a) != len(b):
        raise ValueError(
            "Vectors must have equal length."
        )

    return sum(
        abs(x - y)
        for x, y in zip(a, b)
    )


def l2_distance(
    a: Sequence[float],
    b: Sequence[float],
) -> float:
    """
    Compute Euclidean distance.
    """

    if len(a) != len(b):
        raise ValueError(
            "Vectors must have equal length."
        )

    return math.sqrt(
        sum(
            (x - y) ** 2
            for x, y in zip(a, b)
        )
    )


def entropy(
    probabilities: Sequence[float],
) -> float:
    """
    Shannon entropy.

    Useful for uncertainty measurements.
    """

    result = 0.0

    for probability in probabilities:
        if probability > 0:
            result -= (
                probability
                * math.log(probability)
            )

    return result


__all__ = [
    "sigmoid",
    "softmax",
    "normalize",
    "normalize_dict",
    "weighted_average",
    "clamp",
    "l1_distance",
    "l2_distance",
    "entropy",
]
