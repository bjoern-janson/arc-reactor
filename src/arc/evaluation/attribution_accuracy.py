"""
ARC Attribution Accuracy Evaluation

Implements Weighted Attribution Accuracy (AE_w).

AE_w measures whether an ARC controller correctly identifies
the structural depth at which reality invalidated an assumption.

Formula:

    AE_w =
        1 -
        (Σ W_i |L_i - L_hat_i|)
        --------------------------
        (Σ W_i L_i)

Where:

    L_i:
        Ground-truth failure depth.

    L_hat_i:
        Predicted failure depth.

    W_i:
        Severity weighting based on dependency breadth,
        irreversibility, and downstream impact.

High AE_w:
    Correct causal localization.

Low AE_w:
    Misattribution or blind adaptation.
"""

from typing import Dict, Iterable


def weighted_attribution_accuracy(
    true_layers: Dict[str, float],
    predicted_layers: Dict[str, float],
    weights: Dict[str, float],
) -> float:
    """
    Compute weighted attribution accuracy.

    Args:

        true_layers:
            Ground-truth structural failure depths.

        predicted_layers:
            ARC inferred failure depths.

        weights:
            Severity weights for each structural layer.

    Returns:

        AE_w score in [0, 1].

    Raises:

        ValueError:
            If inputs are invalid or denominator is zero.
    """

    if not true_layers:
        raise ValueError(
            "True layer distribution cannot be empty."
        )

    if set(true_layers) != set(predicted_layers):
        raise ValueError(
            "True and predicted layers must match."
        )

    if set(true_layers) != set(weights):
        raise ValueError(
            "Layer weights must match layer definitions."
        )

    numerator = 0.0
    denominator = 0.0

    for layer in true_layers:

        true_depth = true_layers[layer]
        predicted_depth = predicted_layers[layer]
        weight = weights[layer]

        if true_depth < 0 or predicted_depth < 0:
            raise ValueError(
                "Layer depths must be non-negative."
            )

        if weight < 0:
            raise ValueError(
                "Weights must be non-negative."
            )

        numerator += (
            weight
            * abs(true_depth - predicted_depth)
        )

        denominator += (
            weight
            * true_depth
        )

    if denominator == 0:
        raise ValueError(
            "Attribution denominator cannot be zero."
        )

    score = 1 - (numerator / denominator)

    # Numerical protection
    return max(
        0.0,
        min(1.0, score)
    )


def attribution_error(
    true_layers: Dict[str, float],
    predicted_layers: Dict[str, float],
) -> float:
    """
    Compute unweighted attribution distance.

    Useful for diagnostics when severity weights
    are intentionally removed.
    """

    if set(true_layers) != set(predicted_layers):
        raise ValueError(
            "Layer definitions must match."
        )

    return sum(
        abs(
            true_layers[layer]
            - predicted_layers[layer]
        )
        for layer in true_layers
    )


def attribution_confidence(
    posterior: Dict[str, float],
) -> float:
    """
    Compute FA_c:

        FA_c = max_i P(L_i | E_t)

    Represents confidence in the most likely
    diagnosed failure layer.
    """

    if not posterior:
        raise ValueError(
            "Posterior distribution cannot be empty."
        )

    if any(
        probability < 0
        for probability in posterior.values()
    ):
        raise ValueError(
            "Posterior probabilities cannot be negative."
        )

    total = sum(posterior.values())

    if abs(total - 1.0) > 1e-6:
        raise ValueError(
            "Posterior probabilities must sum to 1."
        )

    return max(posterior.values())
