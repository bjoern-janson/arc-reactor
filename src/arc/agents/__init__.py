"""
ARC Agents

Agent implementations for the Arc Reactor Framework.

The agent layer contains systems evaluated under RAHU:

    - Flat Optimizer
    - Meta Learner
    - ARC-Lite (Oracle Attribution)
    - ARC-Full (Learned Attribution)
    - Oracle Reset (Theoretical Upper Bound)

All agents share a common interface:

    observe()
        ↓
    diagnose()
        ↓
    govern()
        ↓
    intervene()
        ↓
    evaluate()

The purpose of this module is to standardize comparison between
different adaptation strategies under identical environmental shocks.
"""


from .base import ARCBaseAgent

from .flat_optimizer import FlatOptimizer

from .meta_learner import MetaLearner

from .arc_lite import ARCLite

from .arc_controller import ARCController

from .oracle_reset import OracleReset


__all__ = [
    "ARCBaseAgent",
    "FlatOptimizer",
    "MetaLearner",
    "ARCLite",
    "ARCController",
    "OracleReset",
]
