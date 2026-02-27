"""Named mapping presets loaded from YAML config.

Owner: Leo DeRosa
"""

from pathlib import Path
from typing import Any


class MappingProfile:
    """A named preset defining mapping curves, color palettes, and transition speeds."""

    def __init__(self, name: str, params: dict[str, Any]):
        self.name = name
        self.params = params


def load_profiles(config_dir: Path) -> dict[str, MappingProfile]:
    """Load all mapping profiles from YAML files in the config directory."""
    # TODO: scan config_dir for profile YAML files, return dict keyed by name
    raise NotImplementedError
