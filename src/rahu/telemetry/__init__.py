"""
RAHU Telemetry.

The telemetry subsystem records everything required to evaluate
adaptive behavior during RAHU experiments.

Unlike the ARC evaluation package—which defines metrics such as
Recovery Intelligence (RI), Attribution Accuracy (AE_w), or Future
Adaptive Capacity (C_future)—the RAHU telemetry layer is responsible
for collecting, storing, and exporting the raw experimental traces
from which those metrics are computed.

Responsibilities
----------------
- Record per-step agent behavior.
- Record regime transitions and shocks.
- Log attribution outputs.
- Track permeability allocation.
- Track intervention magnitude.
- Preserve complete experiment history.
- Export reproducible experiment logs.

Submodules
----------
logger
    Central experiment logger.

events
    Structured telemetry events.

recorder
    Step-by-step trajectory recording.

export
    Serialization utilities.
"""

from .events import TelemetryEvent
from .logger import TelemetryLogger
from .recorder import EpisodeRecorder

__all__ = [
    "TelemetryEvent",
    "TelemetryLogger",
    "EpisodeRecorder",
]
