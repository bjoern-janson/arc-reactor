"""
Validation Utilities.

Provides schema and configuration validation helpers for ARC/RAHU.

The validation layer protects experiment integrity by ensuring:

    - normalized parameters remain bounded
    - configurations are internally consistent
    - benchmark assumptions are explicit
    - invalid experimental states fail early

This module contains no ARC decision logic.
It only verifies that inputs satisfy declared constraints.
"""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from typing import Any, Iterable, Mapping


def validate_probability(
    value: float,
    name: str = "value",
) -> None:
    """
    Validate a normalized probability/value.

    Expected range:

        0.0 <= value <= 1.0
    """

    if not 0.0 <= value <= 1.0:
        raise ValueError(
            f"{name} must be between 0 and 1. "
            f"Received {value}."
        )


def validate_non_negative(
    value: float,
    name: str = "value",
) -> None:
    """
    Validate non-negative quantities.
    """

    if value < 0:
        raise ValueError(
            f"{name} must be non-negative. "
            f"Received {value}."
        )


def validate_regime_parameters(
    *,
    regime_depth: float,
    dependency_breadth: float,
    shock_frequency: float,
) -> None:
    """
    Validate RAHU ecological variables.

    Checks:

        D_R ∈ [0,1]
        B_D ∈ [0,1]
        F_S ∈ [0,1]
    """

    validate_probability(
        regime_depth,
        "regime_depth",
    )

    validate_probability(
        dependency_breadth,
        "dependency_breadth",
    )

    validate_probability(
        shock_frequency,
        "shock_frequency",
    )


def validate_config(
    config: Any,
) -> None:
    """
    Validate a configuration object.

    Supports dataclass-based configs such as RAHUConfig.
    """

    if not is_dataclass(config):
        raise TypeError(
            "Configuration must be a dataclass instance."
        )

    for field in fields(config):
        value = getattr(
            config,
            field.name,
        )

        if value is None:
            continue

        if isinstance(value, (int, float)):
            if field.name in {
                "regime_depth",
                "dependency_breadth",
                "shock_frequency",
            }:
                validate_probability(
                    value,
                    field.name,
                )


def validate_schema(
    data: Mapping[str, Any],
    required_fields: Iterable[str],
) -> None:
    """
    Validate dictionary schemas.

    Useful for:
        - telemetry payloads
        - experiment exports
        - benchmark definitions
    """

    missing = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing:
        raise ValueError(
            "Missing required fields: "
            + ", ".join(missing)
        )


def validate_agent_type(
    agent_type: str,
    allowed_types: Iterable[str],
) -> None:
    """
    Ensure requested agent exists in benchmark registry.
    """

    if agent_type not in allowed_types:
        raise ValueError(
            f"Unknown agent type '{agent_type}'. "
            f"Available: {list(allowed_types)}"
        )


def validate_shock_type(
    shock_type: str,
    allowed_types: Iterable[str],
) -> None:
    """
    Ensure shock belongs to the supported RAHU suite.
    """

    if shock_type not in allowed_types:
        raise ValueError(
            f"Unknown shock type '{shock_type}'. "
            f"Available: {list(allowed_types)}"
        )


__all__ = [
    "validate_probability",
    "validate_non_negative",
    "validate_regime_parameters",
    "validate_config",
    "validate_schema",
    "validate_agent_type",
    "validate_shock_type",
]
