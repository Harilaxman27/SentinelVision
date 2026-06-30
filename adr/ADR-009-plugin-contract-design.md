# ADR-009: Plugin Contract Design

## Status
Accepted

## Context

New retail intelligence capabilities must be addable without modifying core code.

## Decision

Plugins implement PluginBase, provide plugin.yaml and rules.yaml, and are discovered by PluginManager at startup.

## Consequences

Zero core code changes for new capabilities.
