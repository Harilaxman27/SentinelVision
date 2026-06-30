"""
Module: benchmarks.plugin_bench

Purpose:
Micro-benchmark for plugin evaluation latency.

Owner:
SentinelVision
"""

import asyncio
import time
from typing import Any

from backend.events.schemas import TrackUpdateEvent
from backend.plugins.context import PluginContext
from backend.plugins.manager import PluginManager
from backend.plugins.registry import registry
from plugins.shoplifting.plugin import ShopliftingPlugin
from backend.shared.types.geometry import BoundingBox


async def run_benchmark() -> None:
    # 1. Setup
    plugin = ShopliftingPlugin()
    registry.register(plugin)
    
    manager = PluginManager("/tmp/nonexistent") # Mock
    await manager.initialize_all()

    bbox = BoundingBox(x1=0, y1=0, x2=100, y2=100, confidence=0.9, class_id=0, class_name="person")
    event = TrackUpdateEvent(
        event_id="bench-1",
        source="bench",
        camera_id="cam_1",
        track_id=1,
        bbox=bbox,
        frame_sequence=1,
    )
    
    context = PluginContext(
        current_event=event,
        camera_id="cam_1",
        config={"shoplifting": {"enabled": True, "confidence_threshold": 0.5}}
    )

    # 2. Warmup
    for _ in range(100):
        await manager.dispatch_event(context)

    # 3. Benchmark
    iterations = 10000
    start_time = time.perf_counter()
    
    for _ in range(iterations):
        await manager.dispatch_event(context)
        
    end_time = time.perf_counter()
    duration = end_time - start_time
    
    ops_per_sec = iterations / duration
    print(f"Plugin Evaluation Benchmark")
    print(f"Iterations: {iterations}")
    print(f"Total time: {duration:.4f} seconds")
    print(f"Ops/sec:    {ops_per_sec:.2f}")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
