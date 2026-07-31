"""
Serialization Utilities.

Provides reproducible export and import helpers for ARC/RAHU
experiments.

Supported formats:

    - JSON
    - YAML (optional dependency)

Used for:
    - telemetry archives
    - experiment configurations
    - benchmark results
    - reproducibility snapshots

The serialization layer intentionally contains no ARC or RAHU logic.
It only converts structured data into persistent representations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Union


PathLike = Union[str, Path]


def save_json(
    data: Any,
    path: PathLike,
    *,
    indent: int = 2,
) -> None:
    """
    Save data as JSON.

    Parameters
    ----------
    data:
        JSON-compatible object.

    path:
        Destination file path.
    """

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=indent,
            ensure_ascii=False,
        )


def load_json(
    path: PathLike,
) -> Any:
    """
    Load JSON data.
    """

    path = Path(path)

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def save_yaml(
    data: Dict[str, Any],
    path: PathLike,
) -> None:
    """
    Save data as YAML.

    Requires PyYAML.

    YAML is useful for:
        - experiment configs
        - human-readable parameters
        - benchmark sweeps
    """

    try:
        import yaml
    except ImportError as exc:
        raise ImportError(
            "PyYAML is required for YAML export. "
            "Install with: pip install pyyaml"
        ) from exc

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        yaml.safe_dump(
            data,
            file,
            sort_keys=False,
        )


def load_yaml(
    path: PathLike,
) -> Dict[str, Any]:
    """
    Load YAML data.
    """

    try:
        import yaml
    except ImportError as exc:
        raise ImportError(
            "PyYAML is required for YAML import. "
            "Install with: pip install pyyaml"
        ) from exc

    path = Path(path)

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return yaml.safe_load(file)


def serialize_dataclass(
    obj: Any,
) -> Dict[str, Any]:
    """
    Convert dataclass objects into dictionaries.

    Useful for:
        - RAHUConfig
        - TelemetryEvent
        - ExperimentResult
    """

    from dataclasses import asdict, is_dataclass

    if not is_dataclass(obj):
        raise TypeError(
            "Object must be a dataclass instance."
        )

    return asdict(obj)


def save_experiment_snapshot(
    snapshot: Dict[str, Any],
    directory: PathLike,
    name: str,
) -> None:
    """
    Save a complete experiment snapshot.

    Creates:

        directory/
            name.json

    Intended for reproducible benchmark checkpoints.
    """

    directory = Path(directory)

    save_json(
        snapshot,
        directory / f"{name}.json",
    )


__all__ = [
    "save_json",
    "load_json",
    "save_yaml",
    "load_yaml",
    "serialize_dataclass",
    "save_experiment_snapshot",
]
