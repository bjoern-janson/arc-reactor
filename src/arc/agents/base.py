"""
ARC Agent Base Interface

Defines the universal agent contract used throughout the
Arc Reactor Framework.

Every compliant ARC agent must implement the adaptive loop:

    Observe Reality
          ↓
    Diagnose Failure
          ↓
    Decide Permission
          ↓
    Allocate Plasticity
          ↓
    Execute Correction
          ↓
    Preserve Future Capacity

The base interface intentionally separates:

    Learning:
        How parameters change.

    ARC Governance:
        Whether, where, and how much change is allowed.

This enables direct comparison between:
    - Flat optimizers
    - Meta learners
    - ARC controllers
    - Oracle systems
"""


from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class AgentState:
    """
    Generic internal agent state.

    Concrete agents may extend this with:
    - neural parameters
    - symbolic representations
    - causal graphs
    - memory structures
    """

    parameters: Dict[str, Any] = field(default_factory=dict)

    representation: Dict[str, Any] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AttributionOutput:
    """
    Required ARC diagnostic output.

    Every ARC-compatible agent must expose
    its belief about failure location.
    """

    failure_posterior: Dict[str, float]

    confidence: float

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Intervention:
    """
    Proposed structural modification.

    Represents:

        ΔS_i = λ_A · Π_A(L_i) · ΔS_max

    """

    layer: str

    magnitude: float

    metadata: Dict[str, Any] = field(default_factory=dict)


class ARCBaseAgent(ABC):
    """
    Abstract ARC agent interface.

    The benchmark interacts with agents only through
    this contract, ensuring fair comparison.
    """

    def __init__(self):
        self.state = AgentState()

        self.last_attribution: Optional[
            AttributionOutput
        ] = None

        self.last_intervention: Optional[
            Intervention
        ] = None

    @abstractmethod
    def observe(
        self,
        observation: Any,
    ) -> None:
        """
        Process new environmental information.

        Equivalent to:

            Γ → E_t
        """
        pass

    @abstractmethod
    def diagnose(
        self,
    ) -> AttributionOutput:
        """
        Estimate:

            P(L_i | E_t)

        """
        pass

    @abstractmethod
    def decide_permission(
        self,
    ) -> float:
        """
        Compute global plasticity permission:

            λ_A ∈ [0,1]

        """
        pass

    @abstractmethod
    def allocate_plasticity(
        self,
    ) -> Dict[str, float]:
        """
        Compute spatial allocation:

            Π_A(L_i)

        """
        pass

    @abstractmethod
    def intervene(
        self,
        allocation: Dict[str, float],
        permission: float,
    ) -> Intervention:
        """
        Execute controlled correction:

            ΔS
        """
        pass

    @abstractmethod
    def evaluate(
        self,
    ) -> Dict[str, float]:
        """
        Return evaluation telemetry.

        Expected metrics:

        - AE_w
        - S_retained
        - RI
        - C_future
        """
        pass

    def step(
        self,
        observation: Any,
    ) -> Intervention:
        """
        Execute one complete ARC cycle.

        Pipeline:

            Observe
              ↓
            Diagnose
              ↓
            Permission
              ↓
            Allocation
              ↓
            Intervention
        """

        self.observe(observation)

        attribution = self.diagnose()

        self.last_attribution = attribution

        permission = self.decide_permission()

        allocation = self.allocate_plasticity()

        intervention = self.intervene(
            allocation,
            permission,
        )

        self.last_intervention = intervention

        return intervention
