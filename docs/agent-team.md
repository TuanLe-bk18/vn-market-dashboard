# Agent Team Specification

How the AI agents collaborated on this project (module 3: agent team
coordination).

## Team

| Agent | Role | Responsibilities |
|---|---|---|
| Orchestrator | Planning & integration | Owns `product-spec.md` and `openapi.yaml`; breaks work into GitHub issues; reviews every change against the spec; assembles the final submission. |
| Backend Coder | API + storage | Implements FastAPI endpoints exactly per `openapi.yaml`; SQLite schema and seed data; keeps `backend/` dependency-light. |
| Frontend Coder | UI | Single-page app in `frontend/`; vanilla JS `fetch` against the API contract; no build step. |
| QA | Tests + containers | Writes `tests/test_api.py`; verifies `pytest -q`, `docker compose up --build`, and the CI workflow on a fresh clone. |
| Scribe | Docs | `README.md`, `AGENTS.md`, this file, and `docs/ai-usage-report.md`; keeps docs in sync with code. |

## Coordination process

1. **Contract first:** Orchestrator freezes `openapi.yaml` v0.1 before any
   coder starts. Contract changes are announced as a new issue; coders pause
   affected work until the YAML is updated.
2. **Issue-driven:** one GitHub issue per user story (see `product-spec.md`
   acceptance criteria). The assigned agent references the issue number in
   commits; the Orchestrator moves the card Backlog → Doing → Done.
3. **File-based handoff:** agents communicate through the repo, not chat
   memory — spec, YAML, and code are the shared state. A coder blocked by an
   unclear contract opens an issue instead of guessing.
4. **Review gate:** Backend/Frontend changes are reviewed by the Orchestrator
   against `AGENTS.md` (definition of done) before merge. QA runs the full
   suite + docker build on every PR via CI.
5. **Human in the loop:** the owner approves scope changes (spec non-goals),
   the public deploy, and the final submission. Agents never push to `main`
   directly.

## Tooling

- Task tracker: GitHub Projects (public link in README).
- CI: GitHub Actions (`.github/workflows/ci.yml`) — pytest on every push/PR.
- Runtime: Docker Compose (app + SQLite volume), Render `render.yaml` for the
  public deploy.
