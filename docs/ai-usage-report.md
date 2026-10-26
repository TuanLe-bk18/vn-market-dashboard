# AI Usage Report

How AI was used to build this project — written DURING the work, not after
(module requirement). Each entry: task given to the AI, context provided, how
the output was reviewed/tested, and what was wrong + fixed.

## Entry template

### YYYY-MM-DD — <task>
- **Prompt / task given:** <what was asked, verbatim-ish>
- **Context provided:** <files, specs, constraints handed to the AI>
- **Review:** <how the output was checked: tests run, spec diff, manual test>
- **AI mistakes & fixes:** <what was wrong and how it was corrected>

---

## 2026-10-23 — Project scaffold (FastAPI + SQLite + static frontend)
- **Prompt / task given:** "Scaffold a FastAPI backend serving a bundled market
  snapshot JSON plus a SQLite-backed watchlist CRUD, a dependency-free static
  frontend, pytest suite, Dockerfile + compose, GitHub Actions CI, and English
  docs (README, product-spec, AGENTS.md, agent-team) per the AI Dev Tools
  Project 1 rubric."
- **Context provided:** `product-spec.md` draft, rubric checklist (12 criteria /
  24 points, pass at 10), existing local OHLCV store layout, LIQ screener rule
  for the breadth universe.
- **Review:** `pytest -q` green; `python -m py_compile` on all sources;
  `openapi.yaml` parsed and cross-checked against implemented routes;
  `docker build` smoke-tested (compose run pending).
- **AI mistakes & fixes:** (1) First breadth calc used the full 1,518-ticker
  universe instead of the LIQ screener the pipeline uses — fixed by porting the
  screener rule (price 2k–500k, VOL MA20 50k–200M), snapshot now matches the
  daily report (B20 64.2 / B50 48.0 / B200 26.0). (2) Compose mounted a volume
  over `/app/data`, which would have shadowed the bundled snapshot/seed files
  in the image — fixed by moving the DB volume to `/app/dbdata`.

## (continue below as work progresses)
