# ADR-008: Multiprocessing for Camera Workers

## Status
Accepted

## Context

Inference is CPU-bound. Python GIL prevents true parallelism with threads.

## Decision

Each Camera Worker runs as an isolated OS process via Python multiprocessing.

## Consequences

GIL bypassed. A worker crash cannot affect other cameras.
