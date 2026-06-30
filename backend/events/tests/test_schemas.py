"""
Module: tests.events.schemas

Purpose:
Unit tests for Event schemas serialization and parsing.

Owner:
SentinelVision
"""

import json

import pytest
from pydantic import ValidationError

from backend.events.schemas import (
    EVENT_REGISTRY,
    ReIDMatchEvent,
    TrackLostEvent,
    TrackUpdateEvent,
    parse_event,
)
from backend.shared.types.geometry import BoundingBox


def test_track_update_event() -> None:
    """Test serialising and parsing a TrackUpdateEvent."""
    bbox = BoundingBox(x1=10.0, y1=20.0, x2=100.0, y2=200.0, confidence=0.9, class_id=0, class_name="person")
    
    event = TrackUpdateEvent(
        event_id="test-uuid",
        source="camera_worker_01",
        camera_id="cam_01",
        track_id=1,
        bbox=bbox,
        frame_sequence=100,
        trail_points=[(10.0, 20.0), (12.0, 22.0)]
    )
    
    json_str = event.to_json_str()
    assert '"event_type":"track_update"' in json_str
    assert '"camera_id":"cam_01"' in json_str
    
    parsed = parse_event(json_str)
    assert isinstance(parsed, TrackUpdateEvent)
    assert parsed.track_id == 1
    assert parsed.bbox.confidence == 0.9


def test_parse_invalid_event() -> None:
    """Test parsing failures."""
    # Unknown type
    with pytest.raises(ValueError, match="Unknown or missing event_type"):
        parse_event('{"event_type": "unknown_type", "event_id": "1"}')
        
    # Missing type
    with pytest.raises(ValueError, match="Unknown or missing event_type"):
        parse_event('{"event_id": "1"}')
        
    # Invalid schema for type
    with pytest.raises(ValidationError):
        parse_event('{"event_type": "track_lost", "event_id": "1"}') # missing required fields


def test_registry_coverage() -> None:
    """Ensure all event schemas are in the registry."""
    from backend.events.schemas import BaseEvent
    
    # We can inspect the subclasses of BaseEvent if we wanted, 
    # but practically we just ensure the registry has items.
    assert "track_update" in EVENT_REGISTRY
    assert "track_lost" in EVENT_REGISTRY
    assert "reid_match" in EVENT_REGISTRY
    assert "plugin_trigger" in EVENT_REGISTRY
