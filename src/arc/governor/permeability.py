"""
ARC Structural Permeability Controller

Implements the spatial plasticity allocation mechanism (Π_A).

The permeability controller determines where permitted structural change
should be applied after the permission gate (λ_A) has approved adaptation.

Core principle:
    Change the lowest sufficient layer.

Π_A is normalized across structural layers:
    Σ Π_A(L_i) = 1

The controller incorporates:
- failure posterior P(L_i | E_t)
- attribution confidence FA_c
- economic advantage AAR*
- intervention cost C(L_i)

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class LayerCost:
    """
    Structural intervention cost for a layer.

    Higher values represent deeper, more irreversible changes.
    """

    cost: float

    def __post_init__(self) -> None:
        if self.cost <= 0:
            raise ValueError("Layer intervention cost must be positive.")


class PermeabilityController:
    """
    Computes normalized structural permeability allocation.

    Implements:

        Π_A(L_i) =
        weighted_i / Σ weighted_j

    where:

        weighted_i =
            P(L_i | E_t) * FA_c * AAR* / C(L_i)

    """

    def __init__(self, layer_costs: Dict[str, LayerCost]):
        if not layer_costs:
            raise ValueError("At least one structural layer is required.")

        self.layer_costs = layer_costs

    def compute(
        self,
        failure_posterior: Dict[str, float],
        attribution_confidence: float,
        attribution_advantage_ratio: float,
    ) -> Dict[str, float]:
        """
        Compute normalized permeability allocation.

        Args:
            failure_posterior:
                Probability distribution over failure layers.

            attribution_confidence:
                FA_c value representing diagnostic confidence.

            attribution_advantage_ratio:
                AAR* economic justification for intervention.

        Returns:
            Dictionary mapping layers to Π_A allocation.
        """

        self._validate_inputs(
            failure_posterior,
            attribution_confidence,
            attribution_advantage_ratio,
        )

        raw_weights = {}

        for layer, probability in failure_posterior.items():
            if layer not in self.layer_costs:
                raise KeyError(
                    f"No intervention cost defined for layer '{layer}'."
                )

            raw_weights[layer] = (
                probability
                * attribution_confidence
                * attribution_advantage_ratio
                / self.layer_costs[layer].cost
            )

        total_weight = sum(raw_weights.values())

        if total_weight == 0:
            return {
                layer: 0.0
                for layer in failure_posterior
            }

        return {
            layer: weight / total_weight
            for layer, weight in raw_weights.items()
        }

    @staticmethod
    def _validate_inputs(
        failure_posterior: Dict[str, float],
        attribution_confidence: float,
        attribution_advantage_ratio: float,
    ) -> None:
        """
        Validate controller inputs.
        """

        if not failure_posterior:
            raise ValueError("Failure posterior cannot be empty.")

        if any(
            probability < 0
            for probability in failure_posterior.values()
        ):
            raise ValueError(
                "Failure probabilities must be non-negative."
            )

        probability_sum = sum(failure_posterior.values())

        if abs(probability_sum - 1.0) > 1e-6:
            raise ValueError(
                "Failure posterior must sum to 1."
            )

        if not 0 <= attribution_confidence <= 1:
            raise ValueError(
                "Attribution confidence must be between 0 and 1."
            )

        if attribution_advantage_ratio < 0:
            raise ValueError(
                "Attribution advantage ratio must be non-negative."
            )
