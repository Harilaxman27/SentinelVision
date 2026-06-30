# ADR-002: ByteTrack over DeepSORT

## Status
Accepted

## Context

Multi-object tracking is required within each camera view.

## Decision

Use ByteTrack. It tracks low-confidence detections and does not require per-frame ReID.

## Consequences

Lower CPU usage. Better occlusion handling.
