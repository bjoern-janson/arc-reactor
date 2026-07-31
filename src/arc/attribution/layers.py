"""
ARC Structural Layer Model

Defines the structural hierarchy used by the attribution system.

ARC assumes that adaptive systems are not uniformly plastic.
Different components exist at different levels of structural depth:

    θ  →  M  →  G/O  →  C  →  Ω

where:

    θ  = Parameters
    M  = Representation
    G/O = Rules and operators
    C  = World model / causal assumptions
    Ω  = Ontological assumptions

The layer model provides the structural metadata required for:

    - Regime Depth (D_R)
    - Intervention Cost C(L_i)
    - Plasticity Allocation Π_A(L_i)
"""

from dataclasses import dataclass
from enum import Enum


class StructuralLayer(Enum):
    """
    ARC modification hierarchy.

    Ordered from shallow to deep.
    """

    PARAMETER = "theta"
    REPRESENTATION = "M"
    RULE = "G_O"
    WORLD_MODEL = "C"
    ONTOLOGY = "Omega"


@dataclass(frozen=True)
class LayerProperties:
    """
    Structural properties of an ARC layer.

    Attributes:
        depth:
            Relative abstraction depth.

        dependency:
            Downstream dependency breadth.

        irreversibility:
            Cost of reversing an incorrect modification.

        intervention_cost:
            Estimated modification resistance C(L_i).
    """

    depth: float
    dependency: float
    irreversibility: float
    intervention_cost: float


LAYER_PROPERTIES = {
    StructuralLayer.PARAMETER: LayerProperties(
        depth=0.1,
        dependency=0.2,
        irreversibility=0.1,
        intervention_cost=0.1,
    ),

    StructuralLayer.REPRESENTATION: LayerProperties(
        depth=0.3,
        dependency=0.5,
        irreversibility=0.3,
        intervention_cost=0.3,
    ),

    StructuralLayer.RULE: LayerProperties(
        depth=0.5,
        dependency=0.7,
        irreversibility=0.5,
        intervention_cost=0.5,
    ),

    StructuralLayer.WORLD_MODEL: LayerProperties(
        depth=0.75,
        dependency=0.85,
        irreversibility=0.75,
        intervention_cost=0.75,
    ),

    StructuralLayer.ONTOLOGY: LayerProperties(
        depth=1.0,
        dependency=1.0,
        irreversibility=1.0,
        intervention_cost=1.0,
    ),
}


def regime_depth(
    layer: StructuralLayer,
    alpha: float = 1 / 3,
    beta: float = 1 / 3,
    gamma: float = 1 / 3,
) -> float:
    """
    Calculate unified regime depth:

        D_R(L_i) =
            α Depth(L_i)
          + β Dependency(L_i)
          + γ Irreversibility(L_i)

    Returns:
        Normalized regime depth value.
    """

    properties = LAYER_PROPERTIES[layer]

    return (
        alpha * properties.depth
        + beta * properties.dependency
        + gamma * properties.irreversibility
    )


def intervention_cost(
    layer: StructuralLayer,
) -> float:
    """
    Return structural intervention cost:

        C(L_i)
    """

    return LAYER_PROPERTIES[layer].intervention_cost
