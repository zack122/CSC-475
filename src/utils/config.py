"""YAML configuration loader with Pydantic validation."""

from pathlib import Path
from typing import Any


def load_config(path: Path | str = "config/default.yaml") -> dict[str, Any]:
    """Load and validate the YAML config file, returning a plain dict."""
    # TODO: open YAML, parse with pyyaml, optionally validate with pydantic
    raise NotImplementedError
