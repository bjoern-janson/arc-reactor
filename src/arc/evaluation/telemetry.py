"""
ARC Evaluation Telemetry

Provides structured telemetry collection for the Arc Reactor Framework.

Telemetry tracks the complete adaptive control loop:

    Γ → P(L_i | E_t) → FA_c → λ_A → Π_A → ΔS → RI → C_future

The purpose of telemetry is not only to measure performance recovery,
but to determine whether recovery preserves future adaptive capacity.

Tracked signals:
- Reality coupling strength (Γ)
- Failure attribution posterior
- Attribution confidence (FA_c)
- Attribution accuracy (AE_w)
- Attribution advantage ratio (AAR*)
- Permission amplitude (λ_A)
- Permeability allocation (Π_A)
- Intervention magnitude (ΔS)
- Structural retention (S_retained)
- Recovery intelligence (RI)
- Future capacity (C_future)

The telemetry layer intentionally remains independent from control logic.
It observes decisions; it does not make them.
"""


from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time


@dataclass
class TelemetryEvent:
    """
    Single ARC control-cycle observation.
    """

    timestamp: float = field(default_factory=time.time)

    # Reality coupling
    gamma: Optional[float] = None

    # Attribution state
    failure_posterior: Dict[str, float] = field(default_factory=dict)
    attribution_confidence: Optional[float] = None
    attribution_accuracy: Optional[float] = None

    # Economic governance
    aar: Optional[float] = None

    # Plasticity governance
    permission_lambda: Optional[float] = None
    permeability_allocation: Dict[str, float] = field(default_factory=dict)

    # Structural intervention
    intervention_delta: Dict[str, float] = field(default_factory=dict)

    # Evaluation metrics
    viability_post: Optional[float] = None
    structural_retention: Optional[float] = None
    recovery_intelligence: Optional[float] = None
    future_capacity: Optional[float] = None

    metadata: Dict[str, object] = field(default_factory=dict)


class TelemetryRecorder:
    """
    Records ARC execution traces.

    The recorder enables:
    - post-hoc analysis
    - phase boundary discovery
    - attribution debugging
    - comparison between agents
    """

    def __init__(self):
        self.events: List[TelemetryEvent] = []

    def record(self, event: TelemetryEvent) -> None:
        """
        Store a telemetry event.
        """
        self.events.append(event)

    def latest(self) -> Optional[TelemetryEvent]:
        """
        Return most recent telemetry state.
        """
        if not self.events:
            return None

        return self.events[-1]

    def clear(self) -> None:
        """
        Reset telemetry history.
        """
        self.events.clear()

    def export(self) -> List[dict]:
        """
        Export telemetry history as serializable dictionaries.
        """
        return [
            {
                "timestamp": event.timestamp,
                "gamma": event.gamma,
                "failure_posterior": event.failure_posterior,
                "attribution_confidence": event.attribution_confidence,
                "attribution_accuracy": event.attribution_accuracy,
                "aar": event.aar,
                "permission_lambda": event.permission_lambda,
                "permeability_allocation": event.permeability_allocation,
                "intervention_delta": event.intervention_delta,
                "viability_post": event.viability_post,
                "structural_retention": event.structural_retention,
                "recovery_intelligence": event.recovery_intelligence,
                "future_capacity": event.future_capacity,
                "metadata": event.metadata,
            }
            for event in self.events
        ]

    def metric_series(self, metric: str) -> List[float]:
        """
        Extract a time series for a telemetry metric.

        Example:
            telemetry.metric_series("future_capacity")
        """
        values = []

        for event in self.events:
            value = getattr(event, metric, None)

            if value is not None:
                values.append(value)

        return values


def compare_future_capacity(
    events: List[TelemetryEvent],
) -> bool:
    """
    Validate the ARC future-capacity invariant:

        C_future(t+1) >= C_future(t)

    Returns:
        True if capacity is preserved or expanded.
    """

    capacities = [
        event.future_capacity
        for event in events
        if event.future_capacity is not None
    ]

    if len(capacities) < 2:
        return True

    return all(
        capacities[i + 1] >= capacities[i]
        for i in range(len(capacities) - 1)
    )
