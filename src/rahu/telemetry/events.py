"""
RAHU Telemetry Events.

Defines the immutable data structures used to record benchmark
trajectories.

Telemetry events intentionally store observations, decisions, and
actions without evaluating them. Interpretation belongs to the ARC
evaluation layer.

Core recorded dimensions:

    Reality:
        - environment state
        - regime information
        - shock metadata

    Diagnosis:
        - failure posterior P(L_i | E_t)
        - attribution confidence FA_c

    Governance:
        - permission gate λ_A
        - permeability allocation Π_A
        - intervention magnitude ΔS

    Outcome:
        - reward
        - retention signals
        - future capacity estimates
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class TelemetryEvent:
    """
    Single immutable experiment event.

    Each event represents one recorded transition during a RAHU run.
    """

    step: int

    agent_id: str

    event_type: str

    payload: Dict[str, Any] = field(
        default_factory=dict
    )

    timestamp: Optional[float] = None

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Convenience accessor for payload fields.
        """

        return self.payload.get(
            key,
            default,
        )


@dataclass(frozen=True)
class AttributionEvent:
    """
    Diagnostic telemetry.

    Records the agent's belief about where failure occurred.
    """

    step: int

    posterior: Dict[str, float]

    confidence: float

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(frozen=True)
class GovernanceEvent:
    """
    Plasticity control telemetry.

    Records ARC's self-modification permission and allocation.
    """

    step: int

    permission_lambda: float

    permeability: Dict[str, float]

    intervention: Dict[str, float]

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(frozen=True)
class EnvironmentEvent:
    """
    Environment-side telemetry.

    Records external reality changes.
    """

    step: int

    regime_depth: float

    dependency_breadth: float

    shock_frequency: float

    shock_type: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


__all__ = [
    "TelemetryEvent",
    "AttributionEvent",
    "GovernanceEvent",
    "EnvironmentEvent",
]
