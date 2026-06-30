# ROLE

Continue SentinelVision implementation.

Previous phases already exist.

Do not regenerate them.

Only implement this phase.

---

Read

PROMPT_01_ARCHITECT.md

PROMPT_02_REPOSITORY_BLUEPRINT.md

before coding.

---

DO NOT

Review architecture.

Explain implementation.

Summarize.

Ask approval.

Stop.

Generate placeholders.

Leave unfinished code.

---

IMPLEMENT ONLY

backend/plugins/

plugins/

tests/

security/

benchmarks/

examples/

Developer tooling related to plugins.

Including

Plugin Manager

Plugin Base

Plugin Registry

Manifest validation

Dynamic discovery

Plugin lifecycle

Plugin loading

Dependency validation

Hot reload support if defined

Plugin configuration

Plugin interfaces

Plugin tests

Mock plugins

Pytest fixtures

Coverage configuration

Benchmark scripts

Security validation

Everything production ready.

---

QUALITY RULES

Enterprise quality.

Python 3.12.

100% typed.

SOLID.

No circular imports.

Every interface tested.

Every plugin independently testable.

Every file under 300 lines.

Create additional subfolders whenever required.

No placeholders.

No TODO.

No pass.

No NotImplemented.

---

OUTPUT

Generate implementation immediately.

Implement every file in scope.

Continue automatically until every file is completed.

Never ask questions.

Never wait for approval.

Never summarize.

Finish only when the entire phase is implemented.