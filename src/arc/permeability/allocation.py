"""
ARC Plasticity Allocation

Implements the spatial component of the Arc Reactor control law:

    Π_A(L_i)

Π_A determines where permitted adaptation is directed across
the structural hierarchy.

The allocation mechanism enforces the blast radius conservation law:

    Change the lowest sufficient layer.

Plasticity is distributed according to:

    - failure posterior P(L_i | E_t)
    - attribution confidence FA_c
    - economic advantage AAR*
    - intervention cost C(L_i)

The amplitude gate (λ_A) determines whether change is allowed.
This module determines where that allowed change goes.
"""

from typing import Dict

from .costs import intervention_cost


def raw_permeability_score(
    failure_probability: float,
    attribution_confidence: float,
    aar: float,
    layer: str,
) -> float:
    """
    Compute unnormalized plasticity preference.

    Formula:

        score(L_i) =
            P(L_i|E_t) * FA_c * AAR*
            ------------------------
                  C(L_i)

    """

    cost = intervention_cost(layer)

    if cost <= 0:
        raise ValueError(
            "Intervention cost must be positive."
        )

    return (
        failure_probability
        * attribution_confidence
        * aar
        / cost
    )


def allocate_permeability(
    failure_distribution: Dict[str, float],
    attribution_confidence: float,
    aar: float,
) -> Dict[str, float]:
    """
    Compute normalized spatial plasticity allocation.

    Implements:

        Π_A(L_i) =
            score(L_i)
            -----------
            Σ score(L_j)

    Guarantees:

        Σ Π_A(L_i) = 1

    Args:

        failure_distribution:
            Posterior probability distribution:

                {
                    "theta": p,
                    "representation": p,
                    "grammar": p,
                    "ontology": p
                }

        attribution_confidence:
            FA_c value.

        aar:
            Attribution Advantage Ratio.

    Returns:

        Normalized permeability distribution.
    """

    scores = {
        layer: raw_permeability_score(
            probability,
            attribution_confidence,
            aar,
            layer,
        )
        for layer, probability in failure_distribution.items()
    }

    total = sum(scores.values())

    if total <= 0:
        # No justified intervention.
        return {
            layer: 0.0
            for layer in scores
        }

    return {
        layer: score / total
        for layer, score in scores.items()
    }


def dominant_layer(
    permeability: Dict[str, float],
) -> str | None:
    """
    Return the layer receiving the highest plasticity allocation.

    Useful for telemetry and attribution evaluation.
    """

    if not permeability:
        return None

    return max(
        permeability,
        key=permeability.get,
    )
