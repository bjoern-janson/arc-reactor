"""
Configuration Utilities.

Shared helpers for loading, merging, and managing configuration
objects across ARC and RAHU.

The configuration layer provides the bridge between:

    YAML / JSON experiment definitions
              |
              v
       Python configuration objects
              |
              v
       Reproducible experiment runs

This module contains no benchmark or agent logic.
"""

from __future__ import annotations

from dataclasses import asdict, fields, is_dataclass, replace
from pathlib import Path
from typing import Any, Dict, Type, TypeVar

from .serialization import (
    load_json,
    load_yaml,
)


T = TypeVar(
    "T",
)


def load_config_file(
    path: str | Path,
) -> Dict[str, Any]:
    """
    Load a configuration dictionary from JSON or YAML.

    Format is inferred from file extension.
    """

    path = Path(path)

    suffix = path.suffix.lower()

    if suffix == ".json":
        return load_json(path)

    if suffix in {".yaml", ".yml"}:
        return load_yaml(path)

    raise ValueError(
        f"Unsupported configuration format: {suffix}"
    )


def dataclass_from_dict(
    cls: Type[T],
    values: Dict[str, Any],
) -> T:
    """
    Construct a dataclass from a dictionary.

    Unknown fields are ignored to allow forward-compatible configs.
    """

    if not is_dataclass(cls):
        raise TypeError(
            "Target configuration must be a dataclass."
        )

    valid_fields = {
        field.name
        for field in fields(cls)
    }

    filtered = {
        key: value
        for key, value in values.items()
        if key in valid_fields
    }

    return cls(
        **filtered
    )


def config_to_dict(
    config: Any,
) -> Dict[str, Any]:
    """
    Convert a configuration object into a dictionary.
    """

    if not is_dataclass(config):
        raise TypeError(
            "Configuration must be a dataclass."
        )

    return asdict(config)


def merge_configs(
    base: T,
    overrides: Dict[str, Any],
) -> T:
    """
    Apply overrides to a dataclass configuration.

    Useful for parameter sweeps:

        base config
            +
        changed D_R/B_D/F_S
            =
        new experiment config
    """

    if not is_dataclass(base):
        raise TypeError(
            "Base configuration must be a dataclass."
        )

    valid_fields = {
        field.name
        for field in fields(base)
    }

    updates = {
        key: value
        for key, value in overrides.items()
        if key in valid_fields
    }

    return replace(
        base,
        **updates,
    )


def save_config(
    config: Any,
    path: str | Path,
) -> None:
    """
    Save a configuration snapshot as JSON.

    Intended for experiment reproducibility.
    """

    from .serialization import save_json

    save_json(
        config_to_dict(config),
        path,
    )


def build_sweep(
    config: T,
    parameter: str,
    values: list[Any],
) -> list[T]:
    """
    Create a simple configuration sweep.

    Example:

        build_sweep(
            config,
            "regime_depth",
            [0.1, 0.5, 0.9]
        )

    Used for RAHU phase-boundary experiments.
    """

    results = []

    for value in values:
        results.append(
            merge_configs(
                config,
                {
                    parameter: value,
                },
            )
        )

    return results


__all__ = [
    "load_config_file",
    "dataclass_from_dict",
    "config_to_dict",
    "merge_configs",
    "save_config",
    "build_sweep",
]
