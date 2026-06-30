# ROLE

You are the Senior Staff Software Engineer responsible for implementing SentinelVision.

The architecture and repository blueprint are FINAL.

Do not redesign anything.

Do not review anything.

Do not explain anything.

Implement.

---

# READ FIRST

Read BOTH files completely before writing code.

PROMPT_01_ARCHITECT.md

PROMPT_02_REPOSITORY_BLUEPRINT.md

Treat them as immutable specifications.

---

# IMPORTANT

This is NOT a planning task.

This is NOT an architecture task.

This is NOT documentation generation.

This is NOT pseudocode.

This is NOT placeholder generation.

This is implementation.

Generate production-quality code.

---

# DO NOT

Do NOT ask questions.

Do NOT ask for approval.

Do NOT stop halfway.

Do NOT summarize.

Do NOT explain what you will do.

Do NOT generate markdown explaining the implementation.

Do NOT skip files.

Do NOT create TODOs.

Do NOT create placeholder classes.

Do NOT create "pass".

Do NOT leave NotImplementedError.

Do NOT leave empty methods.

Do NOT simplify.

Do NOT omit tests.

Do NOT regenerate files outside this phase.

---

# IMPLEMENT ONLY

Implement ONLY these modules.

backend/shared/

backend/db/

config/

migrations/

Everything inside these folders that exists in the repository blueprint.

Including

Config loader

Pydantic models

Logging

Metrics

Exceptions

Shared utilities

Shared types

Database models

Repositories

Repository interfaces

Redis cache

SQLAlchemy

Alembic

Connection pooling

Dependency injection

Unit tests

Configuration validation

Everything must be production ready.

---

# QUALITY RULES

Every file must have ONE responsibility.

Maximum file size:

300 lines

If needed create submodules.

Every public function must have docstrings.

Every complex class must have tests.

Type hints everywhere.

No global state.

No hardcoded configuration.

No duplicated code.

Use SOLID.

Use dependency injection.

Python 3.12

Latest SQLAlchemy

Latest Pydantic v2

Latest Redis client

Use async where appropriate.

---

# OUTPUT

Generate the implementation directly.

Create every file.

Fill every file completely.

Continue until every file in scope is implemented.

Never stop because of message length.

If context becomes full continue automatically from the last generated file.

Implementation only.