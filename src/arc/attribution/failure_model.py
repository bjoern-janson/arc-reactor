"""
ARC Failure Attribution Model

Implements probabilistic failure localization:

    P(L_i | E_t)

The failure model answers the diagnostic question:

    "Given evidence from reality, which structural layer
     is most likely invalidated?"

ARC does not directly convert error into updates.

Instead:

    Reality Evidence
        ↓
    Failure Posterior
        ↓
    Attribution Confidence
        ↓
    Governed Plasticity

The output of this module is a probabilistic belief distribution
over structural failure layers.

Example layers:

    θ:
        Parameter calibration failure

    M:
        Representation failure

    G/O:
        Rule or operator failure

    C:
        Core ontology failure
"""


from dataclasses import dataclass, field
from typing import Dict


@dataclass
class FailureEvidence:
    """
    Environmental evidence used for attribution.

    Attributes:

        error_signal:
            Magnitude of observed prediction failure.

        persistence:
            How long the failure persists after attempted correction.

        transfer_failure:
            Whether failure generalizes across contexts.

        representation_conflict:
            Evidence that observations no longer align.

        rule_violation:
            Evidence that the governing function is invalid.
    """

    error_signal: float

    persistence: float = 0.0

    transfer_failure: float = 0.0

    representation_conflict: float = 0.0

    rule_violation: float = 0.0


DEFAULT_PRIORS: Dict[str, float] = {
    "theta": 0.40,
    "representation": 0.30,
    "grammar": 0.20,
    "ontology": 0.10,
}


@dataclass
class FailureModel:
    """
    Bayesian-style failure attribution model.

    Produces:

        P(L_i | E_t)

    across structural layers.
    """

    priors: Dict[str, float] = field(
        default_factory=lambda: DEFAULT_PRIORS.copy()
    )

    def diagnose(
        self,
        evidence: FailureEvidence,
    ) -> Dict[str, float]:
        """
        Estimate failure posterior.

        This implementation is intentionally simple and
        interpretable for RAHU-0.

        Future versions may replace this with:
        - neural attribution models
        - causal graphs
        - learned inference networks
        """

        scores = {
            "theta": self.priors["theta"],
            "representation": self.priors["representation"],
            "grammar": self.priors["grammar"],
            "ontology": self.priors["ontology"],
        }

        # Persistent error suggests deeper failure.
        scores["theta"] *= (
            1.0 + evidence.error_signal
        )

        scores["representation"] *= (
            1.0 + evidence.representation_conflict
        )

        scores["grammar"] *= (
            1.0 + evidence.rule_violation
        )

        scores["ontology"] *= (
            1.0
            + evidence.transfer_failure
            + evidence.persistence
        )

        return self._normalize(scores)

    @staticmethod
    def _normalize(
        scores: Dict[str, float],
    ) -> Dict[str, float]:
        """
        Convert scores into probability distribution.
        """

        total = sum(scores.values())

        if total <= 0:
            raise ValueError(
                "Failure attribution scores must be positive."
            )

        return {
            layer: score / total
            for layer, score in scores.items()
        }


def failure_depth(
    posterior: Dict[str, float],
) -> float:
    """
    Convert failure posterior into continuous regime depth.

    Approximate mapping:

        theta            = 0.25
        representation   = 0.50
        grammar          = 0.75
        ontology         = 1.00

    """

    depth_map = {
        "theta": 0.25,
        "representation": 0.50,
        "grammar": 0.75,
        "ontology": 1.00,
    }

    return sum(
        probability * depth_map[layer]
        for layer, probability in posterior.items()
    )
