# PyB — Python Gap-Fill (30 days)

Fast-paced audit series: fill gaps, modernise idioms, lock in the uv + git + Obsidian + Claude Code workflow.

## Conventions
- Tooling: uv only (uv add / uv run / uv lock / uv sync). Never pip or conda here.
- Workflow: day-branch pattern — create `day-NN`, work, merge to `main`, delete branch.
  The merge to main is the completion signal read by the scheduled task.
- File layout: ONE FOLDER PER DAY, `src/day_NN_topic/` (e.g. `day_03_data_structures/`), containing `exercise.py` and, when the lesson has tests, `test_exercise.py` alongside it in the same folder. Each day's folder is self-contained; never import one day's folder from another. There is no shared top-level tests/ folder — tests live with the day they test.
- Tests: `uv run pytest`  •  Lint/format: `uv run ruff check .` and `uv run ruff format .`
- One exercise per day, delivered as .docx to /Users/derpzoom/Projects/python-mastery/Daily Lessons/.
- Keys live in .env, loaded with load_dotenv(). Never hardcode secrets.

## When helping here
- Explain reasoning, don't just hand over solutions — this is a learning repo.
- Exactly one ??? placeholder per exercise; the HINT section answers it.
