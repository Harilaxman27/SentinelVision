"""
Example SentinelVision Plugin
-----------------------------

This is an example of how to build a simple third-party plugin.
Save this file into the `plugins/` directory to have it automatically
discovered and loaded on startup.
"""

import logging

from backend.plugins.base import BasePlugin, PluginManifest
from backend.plugins.context import PluginContext
from backend.events.schemas import TrackUpdateEvent

logger = logging.getLogger(__name__)


class DummyExamplePlugin(BasePlugin):
    """An example plugin that logs every 10th frame of a track."""

    @property
    def manifest(self) -> PluginManifest:
        return PluginManifest(
            name="example_dummy",
            version="0.1.0",
            description="Logs every 10th frame to demonstrate state usage.",
            author="Developer",
        )

    async def on_load(self) -> None:
        logger.info(f"Loaded {self.manifest.name}")

    async def on_unload(self) -> None:
        logger.info(f"Unloaded {self.manifest.name}")

    async def evaluate(self, context: PluginContext) -> None:
        event = context.current_event
        
        # We only care about track updates
        if not isinstance(event, TrackUpdateEvent):
            return
            
        # Use context state to keep track of counts
        state_key = f"track_{event.track_id}_count"
        count = context.state.get(state_key, 0) + 1
        context.state[state_key] = count
        
        if count % 10 == 0:
            logger.info(f"Track {event.track_id} has been seen {count} times on {context.camera_id}.")
            
            # Optionally emit a trigger (this wouldn't normally be an 'alert', 
            # but demonstrates the API).
            context.emit_trigger(
                plugin_name=self.manifest.name,
                rule_name="tenth_frame_rule",
                confidence=1.0,
                context_data={"count": count}
            )
