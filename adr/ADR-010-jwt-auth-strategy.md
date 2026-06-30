# ADR-010: JWT Authentication Strategy

## Status
Accepted

## Context

Operator authentication is required for the dashboard API.

## Decision

JWT Bearer tokens with 8-hour expiry. Redis-backed revocation list. Role-based access.

## Consequences

Stateless API. Token revocation on operator disable.
