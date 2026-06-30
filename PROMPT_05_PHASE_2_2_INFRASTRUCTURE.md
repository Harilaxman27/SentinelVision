# ROLE

Continue implementing SentinelVision.

Architecture is already approved.

Repository already exists.

Foundation is already implemented.

Continue.

---

Read

PROMPT_01_ARCHITECT.md

PROMPT_02_REPOSITORY_BLUEPRINT.md

before implementation.

---

DO NOT

Review

Redesign

Refactor unrelated code

Modify previous modules

Ask questions

Ask approval

Generate summaries

Stop halfway

---

IMPLEMENT ONLY

docker/

deployment/

monitoring/

scripts/

backend/events/

Infrastructure required by these modules.

Including

Dockerfiles

Docker Compose

Production Compose

Monitoring

Prometheus

Grafana

Loki

AlertManager

Redis Streams

Producer

Consumer

Consumer Groups

Retry

Dead Letter Queue

Event Schemas

Event Bus Interfaces

Health Checks

Startup scripts

Environment loading

Structured logging integration

Integration tests

Everything must compile.

Everything must be production ready.

---

QUALITY RULES

No placeholder code.

No TODO.

No pass.

No NotImplemented.

Maximum file size 300 lines.

Split into submodules whenever necessary.

Every module independently testable.

Every external dependency abstracted.

Every public class documented.

100% typed.

---

OUTPUT

Generate files directly.

Implement every file completely.

Continue automatically until all files in scope are finished.

Never ask before continuing.