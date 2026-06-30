# ADR-001: Layered Architecture (Perception â†’ Event â†’ Decision â†’ Product)

## Status
Accepted

## Context

SentinelVision requires a maintainable, plugin-extensible architecture.

## Decision

Adopt a strict four-layer architecture. Each layer has one responsibility.

## Consequences

New capabilities are added as plugins without changing core layers.
