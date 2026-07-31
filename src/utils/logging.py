"""
Logging Utilities.

Shared logging infrastructure for ARC and RAHU.

Provides consistent experiment logging across:

    - environments
    - agents
    - generators
    - telemetry
    - evaluation pipelines

The logging layer records execution state and debugging information.
It does not replace telemetry, which stores scientific experiment data.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional


DEFAULT_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)


def get_logger(
    name: str,
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Create or retrieve a configured logger.

    Parameters
    ----------
    name:
        Logger namespace.

    level:
        Logging severity threshold.
    """

    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(
            sys.stdout
        )

        formatter = logging.Formatter(
            DEFAULT_FORMAT
        )

        handler.setFormatter(
            formatter
        )

        logger.addHandler(
            handler
        )

    logger.setLevel(level)

    return logger


def configure_logging(
    *,
    level: int = logging.INFO,
    log_file: Optional[str] = None,
) -> None:
    """
    Configure root logging.

    Parameters
    ----------
    level:
        Global logging level.

    log_file:
        Optional persistent log destination.
    """

    handlers = []

    stream_handler = logging.StreamHandler(
        sys.stdout
    )

    stream_handler.setFormatter(
        logging.Formatter(
            DEFAULT_FORMAT
        )
    )

    handlers.append(
        stream_handler
    )

    if log_file is not None:
        path = Path(log_file)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_handler = logging.FileHandler(
            path,
            encoding="utf-8",
        )

        file_handler.setFormatter(
            logging.Formatter(
                DEFAULT_FORMAT
            )
        )

        handlers.append(
            file_handler
        )

    logging.basicConfig(
        level=level,
        handlers=handlers,
        force=True,
    )


def log_experiment_start(
    logger: logging.Logger,
    experiment_name: str,
    seed: Optional[int] = None,
) -> None:
    """
    Log experiment initialization.
    """

    logger.info(
        "Starting experiment '%s' | seed=%s",
        experiment_name,
        seed,
    )


def log_experiment_end(
    logger: logging.Logger,
    experiment_name: str,
) -> None:
    """
    Log experiment completion.
    """

    logger.info(
        "Completed experiment '%s'",
        experiment_name,
    )


def log_metric(
    logger: logging.Logger,
    metric_name: str,
    value: float,
) -> None:
    """
    Log evaluation metric output.
    """

    logger.info(
        "Metric %s = %.6f",
        metric_name,
        value,
    )


__all__ = [
    "get_logger",
    "configure_logging",
    "log_experiment_start",
    "log_experiment_end",
    "log_metric",
]
