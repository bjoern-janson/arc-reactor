"""
ARC Reality Coupling

Implements the Γ component of the ARC control pipeline.

Γ answers:

    "Did reality actually invalidate an internal assumption?"

The coupling layer converts discrepancies between predicted and observed
environmental states into structured evidence for downstream attribution.

It intentionally does not perform:
    - failure localization
    - intervention selection
    - structural updates

Those responsibilities belong to later ARC layers.
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class RealitySignal:
    """
    Structured representation of environmental mismatch.

    Attributes:
        magnitude:
            Strength of observed mismatch.

        observed:
            Actual environmental outcome.

        predicted:
            System expectation before observation.

        context:
            Optional metadata describing the observation source.
    """

    magnitude: float
    observed: Any
    predicted: Any
    context: Optional[dict] = None


class RealityCoupling:
    """
    Reality coupling mechanism (Γ).

    Converts prediction errors into environmental evidence E_t.

    Future implementations may extend this class with:
        - causal discrepancy detection
        - uncertainty estimation
        - multi-modal feedback integration
        - temporal consistency checks
    """

    def __init__(self, threshold: float = 0.0):
        """
        Args:
            threshold:
                Minimum discrepancy required to emit an invalidation signal.
        """
        self.threshold = threshold

    def measure(
        self,
        predicted: Any,
        observed: Any,
        error_function=None,
        context: Optional[dict] = None,
    ) -> RealitySignal:
        """
        Compare internal prediction against environmental reality.

        Args:
            predicted:
                System-generated expectation.

            observed:
                Actual environmental result.

            error_function:
                Optional custom discrepancy function.

            context:
                Additional environmental metadata.

        Returns:
            RealitySignal containing mismatch magnitude and evidence.
        """

        if error_function is None:
            magnitude = self._default_error(predicted, observed)
        else:
            magnitude = float(error_function(predicted, observed))

        return RealitySignal(
            magnitude=magnitude,
            observed=observed,
            predicted=predicted,
            context=context,
        )

    def is_invalidated(self, signal: RealitySignal) -> bool:
        """
        Determines whether reality has provided sufficient evidence
        that an internal assumption may be invalid.

        Returns:
            True if environmental mismatch exceeds threshold.
        """

        return signal.magnitude > self.threshold

    @staticmethod
    def _default_error(predicted: Any, observed: Any) -> float:
        """
        Basic discrepancy estimator.

        Designed as a placeholder.
        Domain-specific environments should provide their own
        error functions.
        """

        try:
            return abs(float(observed) - float(predicted))
        except (TypeError, ValueError):
            return 1.0 if predicted != observed else 0.0
