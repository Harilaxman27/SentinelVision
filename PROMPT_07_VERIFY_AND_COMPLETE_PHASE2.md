# ROLE

You are the Lead Software Engineer continuing development of SentinelVision.

This is NOT a new project.

The repository already exists on disk.

The architecture and repository blueprint have already been approved.

Previous implementation work has already been completed.

Your job is to VERIFY the current implementation and COMPLETE only what is missing.

---

# READ FIRST

Read BOTH attached files completely before doing anything.

1. PROMPT_01_ARCHITECT.md
2. PROMPT_02_REPOSITORY_BLUEPRINT.md

Treat them as the single source of truth.

---

# BEFORE WRITING CODE

Inspect the ENTIRE repository that currently exists on disk.

Do NOT assume anything.

Do NOT trust previous implementation.

Compare the repository against the Repository Blueprint file.

---

# FOR EVERY FILE IN THE BLUEPRINT

Determine its status.

Use ONLY these statuses:

✅ Exists and Production Ready

⚠ Exists but Incomplete

⚠ Exists but Stub

⚠ Exists but Placeholder

❌ Missing

A file is NOT production ready if it contains:

- TODO
- pass
- ...
- NotImplementedError
- Empty class
- Empty function
- Placeholder implementation
- Mock implementation where production code is expected
- Missing validation
- Missing error handling
- Missing tests
- Missing documentation
- Missing type hints

---

# OUTPUT A CHECKLIST FIRST

Produce a checklist grouped by module.

Example:

backend/shared/

✅ loader.py

⚠ schema.py (incomplete)

❌ validator.py (missing)

backend/db/

...

Continue until every file from the blueprint has been checked.

---

# AFTER THE CHECKLIST

Implement ONLY files marked:

❌ Missing

⚠ Stub

⚠ Placeholder

⚠ Incomplete

DO NOT modify files already marked:

✅ Exists and Production Ready

---

# IMPLEMENTATION RULES

Generate production-quality code.

No placeholders.

No TODOs.

No pass.

No NotImplementedError.

Python 3.12.

Latest libraries.

Type hints everywhere.

SOLID principles.

Files should remain under 300 lines whenever practical.

Create additional submodules if necessary.

Generate tests for newly implemented modules.

---

# DO NOT

Do not redesign the architecture.

Do not change folder structure.

Do not rename files.

Do not regenerate completed files.

Do not ask questions.

Do not ask for approval.

Do not summarize.

Do not stop midway.

Continue until every missing or incomplete file has been implemented.
