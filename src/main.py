"""Entry point: wires all components into the main control loop."""

from src.utils.config import load_config
from src.audio.file_source import FileSource
from src.mir.pipeline import FeaturePipeline
from src.mapping.mapper import Mapper
from src.mapping.scene_manager import SceneManager
from src.dmx.osc_client import OSCClient
from src.dashboard.server import DashboardServer
from src.utils.latency import LatencyTracker


def main(config_path: str = "config/default.yaml") -> None:
    config = load_config(config_path)

    audio = FileSource(
        path=config["audio"]["input_path"],
        sr=config["audio"]["sample_rate"],
        frame_length=config["audio"]["frame_length"],
        hop_length=config["audio"]["hop_length"],
    )
    pipeline = FeaturePipeline(config["mir"])
    mapper = Mapper(config["mapping"])
    scene_mgr = SceneManager(config["scenes"])
    osc = OSCClient(
        host=config["osc"]["host"],
        port=config["osc"]["port"],
        address_map=config["osc"]["address_map"],
    )
    dashboard = DashboardServer(
        port=config["dashboard"]["port"],
        push_rate_hz=config["dashboard"]["push_rate_hz"],
    )
    tracker = LatencyTracker()

    osc.connect()
    dashboard.start()

    try:
        for frame in audio.frames():
            t0 = tracker.start()
            features = pipeline.extract(frame, audio.sample_rate())
            dmx = mapper.map(features)
            dmx = scene_mgr.apply(dmx, features.segment_label)
            osc.send(dmx)
            latency = tracker.record(t0)
            dashboard.push(features, dmx, latency)
    except KeyboardInterrupt:
        pass
    finally:
        osc.close()
        dashboard.stop()


if __name__ == "__main__":
    main()
