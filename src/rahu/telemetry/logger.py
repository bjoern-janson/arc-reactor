"""
RAHU Telemetry Logger.

Central logging interface for benchmark experiments.

The logger captures raw adaptive trajectories without imposing
interpretation. Evaluation modules later transform these records into
metrics such as:

    - Attribution Accuracy (AE_w)
    - Recovery Intelligence (RI)
    - Structural Retention
    - Future Capacity

The logger exists to answer:

"What happened during adaptation?"

not:

"Was the adaptation successful?"
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List, Optional

from .events import TelemetryEvent


class TelemetryLogger:
    """
    Stores structured telemetry events for a RAHU run.

    Designed to support:
        - online monitoring
        - post-hoc evaluation
        - experiment replay
        - serialization
    """

    def __init__(
        self,
        experiment_id: Optional[str] = None,
    ):
        self.experiment_id = experiment_id
        self.events: List[TelemetryEvent] = []

    def log(
        self,
        event: TelemetryEvent,
    ) -> None:
        """
        Append a telemetry event.
        """

        self.events.append(event)

    def record(
        self,
        *,
        step: int,
        agent_id: str,
        event_type: str,
        payload: Dict[str, Any],
    ) -> TelemetryEvent:
        """
        Convenience method for creating and storing events.
        """

        event = TelemetryEvent(
            step=step,
            agent_id=agent_id,
            event_type=event_type,
            payload=payload,
        )

        self.log(event)

        return event

    def filter(
        self,
        event_type: str,
    ) -> List[TelemetryEvent]:
        """
        Retrieve events matching a category.
        """

        return [
            event
            for event in self.events
            if event.event_type == event_type
        ]

    def latest(
        self,
    ) -> Optional[TelemetryEvent]:
        """
        Return the most recent telemetry event.
        """

        if not self.events:
            return None

        return self.events[-1]

    def clear(
        self,
    ) -> None:
        """
        Reset telemetry history.
        """

        self.events.clear()

    def export(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Convert telemetry into a JSON-compatible structure.
        """

        return [
            asdict(event)
            for event in self.events
        ]

    def summary(
        self,
    ) -> Dict[str, Any]:
        """
        Basic experiment metadata summary.
        """

        return {
            "experiment_id": self.experiment_id,
            "event_count": len(self.events),
            "event_types": sorted(
                {
                    event.event_type
                    for event in self.events
                }
            ),
        }
