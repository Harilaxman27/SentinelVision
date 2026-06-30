# ADR-006: PostgreSQL as Primary Database

## Status
Accepted

## Context

Durable persistence is required for alerts, persons, operators, and audit logs.

## Decision

PostgreSQL 16 with Alembic migrations and SQLAlchemy async ORM.

## Consequences

ACID compliance. JSONB for plugin config snapshots. pg_vector available for future use.
