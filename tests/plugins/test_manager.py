"""
Module: tests.plugins.test_manager

Purpose:
Unit tests for the PluginManager and Registry.

Owner:
SentinelVision
"""

import pytest

from backend.plugins.base import BasePlugin, PluginManifest
from backend.plugins.context import PluginContext
from backend.plugins.manager import PluginManager
from backend.plugins.registry import registry


class MockPlugin(BasePlugin):
    def __init__(self) -> None:
        self.load_called = False
        self.unload_called = False
        self.eval_called = False

    @property
    def manifest(self) -> PluginManifest:
        return PluginManifest(name="mock_plugin", version="1.0", description="Mock")

    async def on_load(self) -> None:
        self.load_called = True

    async def on_unload(self) -> None:
        self.unload_called = True

    async def evaluate(self, context: PluginContext) -> None:
        self.eval_called = True
        context.state["mock_executed"] = True


@pytest.fixture
def clean_registry():
    """Ensure the global registry is clear before and after each test."""
    registry.clear()
    yield
    registry.clear()


@pytest.mark.asyncio
async def test_plugin_lifecycle(clean_registry) -> None:
    """Test that a plugin can be registered, loaded, evaluated, and unloaded."""
    plugin = MockPlugin()
    registry.register(plugin)
    
    # Verify registration
    assert registry.get("mock_plugin") is plugin
    
    manager = PluginManager(plugin_dir="/non/existent")  # we manually registered
    
    # Test initialisation
    await manager.initialize_all()
    assert plugin.load_called is True
    
    # Test evaluation
    from backend.events.schemas import TrackLostEvent
    from backend.shared.types.geometry import BoundingBox
    event = TrackLostEvent(event_id="1", source="src", camera_id="cam_1", track_id=1, frame_sequence=1)
    
    context = PluginContext(current_event=event, camera_id="cam_1")
    await manager.dispatch_event(context)
    
    assert plugin.eval_called is True
    assert context.state.get("mock_executed") is True
    
    # Test shutdown
    await manager.shutdown_all()
    assert plugin.unload_called is True
    assert registry.get("mock_plugin") is None  # Registry cleared on shutdown
