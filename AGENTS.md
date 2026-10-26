# AGENTS.md — VN Market Dashboard

Working agreement for every contributor to this repo, human or AI agent.

## How we work

1. **Spec first.** `product-spec.md` and `openapi.yaml` are the source of truth.
   Change behavior → update the spec/YAML first, then code. Never let code and
   contract drift.
2. **Small, reviewable changes.** One user story per change; reference the
   GitHub issue number in the commit message.
3. **Tests with behavior.** Every new endpoint or rule ships with a pytest case
   in `tests/`. `pytest -q` must stay green; CI enforces it on push/PR.
4. **No secrets in the repo.** The SQLite DB (`*.db`) is git-ignored. Seed data
   contains public market levels only — never real position sizes or account
   data. If you need a secret locally, use environment variables.
5. **Docs are part of the change.** Update `README.md` when setup or behavior
   changes; log AI usage in `docs/ai-usage-report.md` as you go (prompts,
   context given, what the AI got wrong and how you fixed it).

## Code conventions

- Backend: FastAPI, type hints, Pydantic models for all request/response bodies.
- Frontend: vanilla JS, no build step, `fetch` against `/api/*` per
  `openapi.yaml`. Keep it dependency-free.
- Python: format with `black` defaults (line length 100); no unused imports.

## Definition of done (per issue)

- [ ] Acceptance criteria from `product-spec.md` met
- [ ] `pytest -q` passes locally
- [ ] `docker compose up --build` serves a working app
- [ ] README/docs updated if behavior or setup changed
- [ ] AI-usage report entry added for AI-generated code

## What agents may / may not do

- MAY: scaffold code, write tests, update docs, run the full test suite and the
  docker build locally.
- MAY NOT: push to `main` directly (open a PR; CI must pass), commit `*.db`
  files or any credential, deploy to the public URL without the owner
  confirming.
