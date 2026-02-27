"""Scene transition state machine.

Owner: Leo DeRosa
"""

from src.models import DMXFrame


class SceneManager:
    """Finite state machine that triggers scene crossfades on segment changes."""

    def __init__(self, config: dict):
        self._config = config
        self._current_scene: str = config.get("default_scene", "ambient")
        self._transition_ms: int = config.get("transition_duration_ms", 500)

    def apply(self, dmx: DMXFrame, segment_label: str) -> DMXFrame:
        """Potentially modify the DMXFrame based on scene transitions."""
        # TODO: detect segment change, crossfade between scenes
        raise NotImplementedError

    def current_scene(self) -> str:
        return self._current_scene
