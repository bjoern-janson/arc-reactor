"""
ARC Intervention Cost Model

Implements structural modification resistance:

    C(L_i)

The intervention cost function encodes the Arc Reactor principle:

    Change the lowest sufficient layer.

Deep structural changes should require greater justification because
they risk destroying accumulated structural capital.

Example hierarchy:

    θ       Parameter calibration
    M       Representation layer
    G/O     Functional grammar / operators
    C       Core ontology / assumptions

Higher layers carry greater modification cost.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class LayerCost:
    """
    Structural intervention cost definition.

    Attributes:

        layer:
            Structural layer identifier.

        cost:
            Relative modification resistance.

        irreversibility:
            Estimated difficulty of reversing the intervention.
    """

    layer: str
    cost: float
    irreversibility: float = 0.0


DEFAULT_LAYER_COSTS: Dict[str, LayerCost] = {
    "theta": LayerCost(
        layer="theta",
        cost=1.0,
        irreversibility=0.05,
    ),
    "representation": LayerCost(
        layer="representation",
        cost=3.0,
        irreversibility=0.25,
    ),
    "grammar": LayerCost(
        layer="grammar",
        cost=7.0,
        irreversibility=0.60,
    ),
    "ontology": LayerCost(
        layer="ontology",
        cost=15.0,
        irreversibility=0.90,
    ),
}


def intervention_cost(
    layer: str,
    costs: Dict[str, LayerCost] | None = None,
) -> float:
    """
    Retrieve intervention cost C(L_i).

    Args:

        layer:
            Structural layer being modified.

        costs:
            Optional custom cost model.

    Returns:

        Structural modification cost.
    """

    cost_table = costs or DEFAULT_LAYER_COSTS

    if layer not in cost_table:
        raise ValueError(
            f"Unknown structural layer: {layer}"
        )

    return cost_table[layer].cost


def normalized_costs(
    costs: Dict[str, LayerCost] | None = None,
) -> Dict[str, float]:
    """
    Convert intervention costs into normalized weights.

    Useful for comparing layers across environments.
    """

    cost_table = costs or DEFAULT_LAYER_COSTS

    maximum = max(
        item.cost
        for item in cost_table.values()
    )

    if maximum <= 0:
        raise ValueError(
            "Maximum intervention cost must be positive."
        )

    return {
        layer: item.cost / maximum
        for layer, item in cost_table.items()
    }


def structural_resistance(
    layer: str,
    costs: Dict[str, LayerCost] | None = None,
) -> float:
    """
    Compute combined modification resistance.

    Resistance incorporates both:

        C(L_i)
        irreversibility(L_i)

    Higher values represent changes that require
    stronger attribution confidence and economic justification.
    """

    cost_table = costs or DEFAULT_LAYER_COSTS

    if layer not in cost_table:
        raise ValueError(
            f"Unknown structural layer: {layer}"
        )

    entry = cost_table[layer]

    return (
        entry.cost
        * (1.0 + entry.irreversibility)
    )
