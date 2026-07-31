"""
RAHU Regime Generators.

Generators are responsible for producing controlled regime shifts used
throughout the RAHU benchmark suite.

Unlike environments, which define interaction dynamics, generators
construct the underlying sequences of environmental change. This allows
the same adaptive task to be evaluated under many different shock
profiles while preserving reproducibility.

Core responsibilities
---------------------

- Generate deterministic or stochastic regime transitions.
- Control regime depth (D_R).
- Control dependency breadth (B_D).
- Control shock frequency (F_S).
- Produce reproducible benchmark sequences.
- Support curriculum and adversarial evaluation.

Example
-------

>>> from rahu.generators import ShockGenerator
>>> generator = ShockGenerator(seed=42)
>>> shock = generator.next_shock()
"""

from .shock_generator import ShockGenerator
from .curriculum import CurriculumGenerator

__all__ = [
    "ShockGenerator",
    "CurriculumGenerator",
]
