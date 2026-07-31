"""
Randomness Utilities.

Centralized random seed management for ARC/RAHU experiments.

Reproducibility is a core requirement of the benchmark system:
identical configurations, seeds, and environments should produce
identical experimental trajectories.

This module provides:

    - global seed initialization
    - reproducible RNG creation
    - seed tracking metadata
    - deterministic experiment setup
"""

from __future__ import annotations

import os
import random
from typing import Dict, Optional

import numpy as np


def set_seed(
    seed: int,
) -> None:
    """
    Set global random seeds.

    Controls:
        - Python random
        - NumPy random generation
        - hash randomization

    Parameters
    ----------
    seed:
        Integer experiment seed.
    """

    os.environ["PYTHONHASHSEED"] = str(seed)

    random.seed(seed)

    np.random.seed(seed)


def create_rng(
    seed: Optional[int] = None,
) -> np.random.Generator:
    """
    Create an isolated NumPy random generator.

    Preferred over global random state for experiments requiring
    independent stochastic components.
    """

    return np.random.default_rng(seed)


def seed_metadata(
    seed: int,
) -> Dict[str, int]:
    """
    Generate reproducibility metadata.

    Stored alongside experiment snapshots.
    """

    return {
        "seed": seed,
    }


class SeedManager:
    """
    Experiment-level seed controller.

    Provides consistent seed allocation across components:

        Environment
        Agent
        Shock Generator
        Evaluation
    """

    def __init__(
        self,
        master_seed: int,
    ):
        self.master_seed = master_seed

        self.rng = np.random.default_rng(
            master_seed
        )

    def child_seed(
        self,
    ) -> int:
        """
        Generate deterministic child seeds.

        Allows independent but reproducible
        subsystem randomness.
        """

        return int(
            self.rng.integers(
                0,
                np.iinfo(np.int32).max,
            )
        )

    def component_seeds(
        self,
    ) -> Dict[str, int]:
        """
        Allocate named subsystem seeds.
        """

        return {
            "environment": self.child_seed(),
            "agent": self.child_seed(),
            "generator": self.child_seed(),
            "evaluation": self.child_seed(),
        }


__all__ = [
    "set_seed",
    "create_rng",
    "seed_metadata",
    "SeedManager",
]
