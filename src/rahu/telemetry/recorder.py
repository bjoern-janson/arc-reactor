"""
RAHU Episode Recorder.

High-level trajectory recorder for benchmark experiments.

The recorder collects the complete causal chain of an adaptive episode:

    Environment
        ↓
    Evidence
        ↓
    Attribution
        ↓
    Governance
        ↓
    Intervention
        ↓
    Outcome

The recorder does not compute evaluation metrics. It preserves the
experimental trace required for later analysis.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .events import (
    AttributionEvent,
    EnvironmentEvent,
    GovernanceEvent,
    TelemetryEvent,
)
from .logger import TelemetryLogger


class EpisodeRecorder:
    """
    Records one complete RAHU experiment episode.
    """

    def __init__(
        self,
        agent_id: str,
        experiment_id: Optional[str] = None,
    ):
        self.agent_id = agent_id

        self.logger = TelemetryLogger(
            experiment_id=experiment_id,
        )

        self.step_count = 0

    def record_environment(
        self,
        event: EnvironmentEvent,
    ) -> None:
        """
        Record environmental state or shock.
        """

        self.logger.record(
            step=event.step,
            agent_id=self.agent_id,
            event_type="environment",
            payload={
                "regime_depth": event.regime_depth,
                "dependency_breadth": event.dependency_breadth,
                "shock_frequency": event.shock_frequency,
                "shock_type": event.shock_type,
                "metadata": event.metadata,
            },
        )

    def record_attribution(
        self,
        event: AttributionEvent,
    ) -> None:
        """
        Record failure diagnosis.
        """

        self.logger.record(
            step=event.step,
            agent_id=self.agent_id,
            event_type="attribution",
            payload={
                "posterior": event.posterior,
                "confidence": event.confidence,
                "metadata": event.metadata,
            },
        )

    def record_governance(
        self,
        event: GovernanceEvent,
    ) -> None:
        """
        Record ARC governance decisions.
        """

        self.logger.record(
            step=event.step,
            agent_id=self.agent_id,
            event_type="governance",
            payload={
                "lambda_A": event.permission_lambda,
                "permeability": event.permeability,
                "intervention": event.intervention,
                "metadata": event.metadata,
            },
        )

    def record_step(
        self,
        *,
        observation: Any,
        action: Any,
        reward: float,
        info: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Record a generic agent-environment transition.
        """

        self.logger.record(
            step=self.step_count,
            agent_id=self.agent_id,
            event_type="transition",
            payload={
                "observation": observation,
                "action": action,
                "reward": reward,
                "info": info or {},
            },
        )

        self.step_count += 1

    def record_intervention(
        self,
        *,
        step: int,
        delta_structure: Dict[str, float],
        reason: Optional[str] = None,
    ) -> None:
        """
        Record executed structural change.
        """

        self.logger.record(
            step=step,
            agent_id=self.agent_id,
            event_type="intervention",
            payload={
                "delta_structure": delta_structure,
                "reason": reason,
            },
        )

    def trajectory(
        self,
    ) -> List[TelemetryEvent]:
        """
        Return raw episode history.
        """

        return self.logger.events

    def export(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Export episode as serializable records.
        """

        return self.logger.export()

    def reset(
        self,
    ) -> None:
        """
        Clear current episode history.
        """

        self.logger.clear()
        self.step_count = 0
