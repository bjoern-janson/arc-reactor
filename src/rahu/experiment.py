"""
RAHU Experiment Runner.

Coordinates the execution of complete RAHU benchmark trials.

The experiment runner connects:

    Configuration
        |
        v
    Environment
        |
        v
    Agent
        |
        v
    Telemetry
        |
        v
    Evaluation

The runner intentionally does not contain ARC logic. It provides the
experimental chamber in which competing adaptive architectures are
tested.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import numpy as np

from .config import RAHUConfig
from .telemetry.recorder import EpisodeRecorder


@dataclass
class ExperimentResult:
    """
    Container for experiment outputs.
    """

    experiment_name: str

    telemetry: list

    metrics: Dict[str, Any]

    metadata: Dict[str, Any]


class RAHUExperiment:
    """
    Executes a single RAHU benchmark experiment.

    Parameters
    ----------
    config:
        Complete experiment configuration.

    environment:
        RAHU environment instance.

    agent:
        Adaptive system being evaluated.
    """

    def __init__(
        self,
        config: RAHUConfig,
        environment: Any,
        agent: Any,
    ):
        self.config = config
        self.environment = environment
        self.agent = agent

        self.rng = np.random.default_rng(
            config.seed
        )

        self.recorder = EpisodeRecorder(
            agent_id=config.agent.agent_type,
            experiment_id=config.experiment_name,
        )

    def reset(self) -> None:
        """
        Reset environment and telemetry state.
        """

        self.recorder.reset()

        if hasattr(self.environment, "reset"):
            self.environment.reset()

        if hasattr(self.agent, "reset"):
            self.agent.reset()

    def step(self) -> Dict[str, Any]:
        """
        Execute one experiment step.

        Expected agent interface:

            action = agent.act(observation)

        Expected environment interface:

            next_state, reward, done, info = env.step(action)
        """

        observation = self.environment.observe()

        action = self.agent.act(
            observation
        )

        result = self.environment.step(
            action
        )

        next_state, reward, done, info = result

        self.recorder.record_step(
            observation=observation,
            action=action,
            reward=reward,
            info=info,
        )

        return {
            "state": next_state,
            "reward": reward,
            "done": done,
            "info": info,
        }

    def run(
        self,
        episodes: int = 1,
        max_steps: int = 1000,
    ) -> ExperimentResult:
        """
        Execute complete experiment.

        Metric computation is intentionally delegated to the evaluation
        layer.
        """

        for _ in range(episodes):

            self.reset()

            for _ in range(max_steps):

                result = self.step()

                if result["done"]:
                    break

        return ExperimentResult(
            experiment_name=(
                self.config.experiment_name
            ),
            telemetry=self.recorder.export(),
            metrics={},
            metadata={
                "seed": self.config.seed,
                "agent": (
                    self.config.agent.agent_type
                ),
            },
        )
