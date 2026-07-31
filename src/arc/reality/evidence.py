"""
ARC Environmental Evidence Representation

Defines E_t: the structured evidence produced when reality coupling
detects a mismatch between internal expectations and environmental outcomes.

The evidence layer acts as the interface between:

    Γ (Reality Coupling)

and:

    P(L_i | E_t) (Failure Attribution)

It contains observations and signals, but does not determine failure depth.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import time


@dataclass
class EnvironmentalEvidence:
    """
    Represents evidence available to the ARC attribution mechanism.

    Attributes:
        prediction:
            The system's prior expectation.

        observation:
            The externally observed outcome.

        discrepancy:
            Magnitude of mismatch between prediction and reality.

        timestamp:
            Time at which evidence was generated.

        context:
            Additional environmental metadata.

        features:
            Optional extracted evidence features for attribution models.
    """

    prediction: Any
    observation: Any
    discrepancy: float

    timestamp: float = field(default_factory=time.time)

    context: Optional[Dict[str, Any]] = None
    features: Optional[Dict[str, Any]] = None

    def is_significant(self, threshold: float = 0.0) -> bool:
        """
        Determines whether this evidence exceeds an invalidation threshold.

        Args:
            threshold:
                Minimum discrepancy required to treat evidence as meaningful.

        Returns:
            True if discrepancy indicates possible invalidation.
        """

        return self.discrepancy > threshold

    def describe(self) -> Dict[str, Any]:
        """
        Returns a serializable representation for telemetry and logging.
        """

        return {
            "prediction": self.prediction,
            "observation": self.observation,
            "discrepancy": self.discrepancy,
            "timestamp": self.timestamp,
            "context": self.context,
            "features": self.features,
        }


def create_evidence(
    prediction: Any,
    observation: Any,
    discrepancy: float,
    context: Optional[Dict[str, Any]] = None,
    features: Optional[Dict[str, Any]] = None,
) -> EnvironmentalEvidence:
    """
    Convenience constructor for generating ARC evidence objects.
    """

    return EnvironmentalEvidence(
        prediction=prediction,
        observation=observation,
        discrepancy=discrepancy,
        context=context,
        features=features,
    )
