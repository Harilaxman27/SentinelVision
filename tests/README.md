# Tests

## Purpose

Cross-module integration, E2E, performance, and stress tests.

## Test Location Rules

| Test Type | Location |
|-----------|----------|
| Unit (single module) | ackend/<module>/tests/ |
| Integration (multi-module) | 	ests/integration/ |
| End-to-End | 	ests/e2e/ |
| Performance | 	ests/performance/ |
| Stress | 	ests/stress/ |

## Running Tests

`ash
pytest tests/                         # all
pytest tests/ -m performance            # performance only
pytest tests/ -m 'not performance'      # exclude performance
`\n