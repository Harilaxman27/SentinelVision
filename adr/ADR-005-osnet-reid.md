# ADR-005: OSNet for Cross-Camera ReID

## Status
Accepted

## Context

Cross-camera person identity resolution is required.

## Decision

Use OSNet. Lightweight, strong CMC-1 performance, OpenVINO exportable.

## Consequences

ReID runs every N frames (configurable) to reduce CPU load.
