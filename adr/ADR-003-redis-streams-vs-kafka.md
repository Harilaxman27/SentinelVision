# ADR-003: Redis Streams over Kafka

## Status
Accepted

## Context

An asynchronous, durable event bus is required between the Perception and Decision layers.

## Decision

Use Redis Streams. Redis is already in the stack for ReID gallery and deduplication.

## Consequences

Simpler operations. Kafka deferred until multi-region is required.
