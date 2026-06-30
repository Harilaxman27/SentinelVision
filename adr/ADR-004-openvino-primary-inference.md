# ADR-004: OpenVINO as Primary Inference Backend

## Status
Accepted

## Context

Minimum hardware is Intel CPU with no GPU.

## Decision

OpenVINO is the primary backend. ONNX Runtime is the fallback for NVIDIA GPU systems.

## Consequences

30-60% lower latency on Intel hardware vs ONNX Runtime CPU.
