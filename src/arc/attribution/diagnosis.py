"""
ARC Failure Attribution Engine

Implements the diagnostic layer:

    E_t → P(L_i | E_t)

The purpose of attribution is not to fix failure.
It determines where reality invalidated the system.

ARC assumes that failures can occur at different structural depths:

    Parameter
        ↓
    Representation
        ↓
    Rule / Operator
        ↓
    World Model
        ↓
    Ontology

The attribution layer produces a probabilistic belief distribution over
these possible failure locations.

Downstream components decide whether and how to intervene.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable

from ..reality.evidence import EnvironmentalEvidence


class FailureLayer(Enum):
    """
    Structural depth hierarchy for ARC attribution.

    Ordered from shallow to deep modification.
    """

    PARAMETER = 1
    REPRESENTATION = 2
    RULE = 3
    WORLD_MODEL = 4
    ONTOLOGY = 5


@dataclass
class FailurePosterior:
    """
    Probability distribution over possible failure layers.

    Represents:

        P(L_i | E_t)
    """

    probabilities: Dict[FailureLayer, float]

    def most_likely(self) -> FailureLayer:
        """
        Returns the layer with highest posterior probability.
        """

        return max(
            self.probabilities,
            key=self.probabilities.get,
        )

    def confidence(self) -> float:
        """
        Attribution confidence:

            FA_c = max_i P(L_i | E_t)
        """

        return max(self.probabilities.values())


class AttributionEngine:
    """
    Base ARC attribution mechanism.

    This implementation provides a simple heuristic baseline.
    Future versions may replace this with:
        - neural causal inference
        - Bayesian models
        - symbolic diagnosis
        - learned attribution networks
    """

    def __init__(
        self,
        layers: Iterable[FailureLayer] = FailureLayer,
    ):
        self.layers = list(layers)

    def diagnose(
        self,
        evidence: EnvironmentalEvidence,
    ) -> FailurePosterior:
        """
        Produce a failure posterior distribution.

        Current implementation is intentionally conservative:
        it does not assume deep failure from large error alone.

        Future implementations should infer from:
            - error signatures
            - intervention history
            - causal dependencies
            - environmental context
        """

        probabilities = self._baseline_distribution()

        if evidence.discrepancy > 0:
            probabilities[FailureLayer.PARAMETER] += 0.1

        return FailurePosterior(
            probabilities=self._normalize(probabilities)
        )

    def _baseline_distribution(self) -> Dict[FailureLayer, float]:
        """
        Initial non-committal attribution prior.
        """

        probability = 1.0 / len(self.layers)

        return {
            layer: probability
            for layer in self.layers
        }

    @staticmethod
    def _normalize(
        probabilities: Dict[FailureLayer, float]
    ) -> Dict[FailureLayer, float]:
        """
        Normalize posterior probabilities.
        """

        total = sum(probabilities.values())

        if total == 0:
            return probabilities

        return {
            key: value / total
            for key, value in probabilities.items()
        }
