# Product Specification — VN Market Dashboard

> Written BEFORE any code, per module 2. Status: draft scaffold — adjust the
> user stories before building further.

## Problem statement

A rules-based retail investor on the Vietnamese stock market needs, before each
session, one screen answering: *may I open positions today, what are my levels,
and is any thesis broken?* Today the answer is spread across chat messages and
a hand-edited markdown table: levels go stale, broken theses linger, and the
market-state check is a separate manual step.

## Users

- Primary: the investor/operator running the strategy (single user, desktop + mobile browser).

## User stories

1. **Market state at a glance.** As the investor, I open the app and within 5
   seconds see VNINDEX, breadth B20/B50/B200, and whether the B200<30 fuse is
   ON, so I know if new entries are allowed today.
   - Acceptance: KPI cards render from `/api/market/summary`; fuse card shows
     ON/OFF with the rule text; data date ("asof") is visible.
2. **Ticker check.** As the investor, I select a watched ticker and see the last
   10 sessions (OHLC, volume, SMA20/50), so I can verify price vs. my levels.
   - Acceptance: `/api/market/tickers/{code}` returns 60 sessions; UI shows the
     last 10; unknown ticker returns 404 with a clear message.
3. **Dynamic watchlist.** As the investor, I add a ticker with thesis,
   resistance, support, and an explicit invalidation condition, so a broken
   level becomes a rewrite task instead of a forgotten hope.
   - Acceptance: POST creates the entry (code upper-cased); the table lists all
     entries; DELETE removes one; entries persist across restarts (SQLite).
4. **One-command run.** As the reviewer, I run `docker compose up --build` and
   the full stack (app + DB) works with no manual steps.
   - Acceptance: fresh clone → one command → http://localhost:8000 usable;
     `pytest -q` passes; CI runs the same suite on every push/PR.

## Non-goals (v1)

- No live intraday prices; the snapshot is refreshed manually via
  `build_snapshot.py` (bundled data keeps the public deploy independent of the
  local cron pipeline).
- No auth/multi-user; single operator.
- No charts library; tables first, charts only if time remains.
- No order execution or broker integration — this is a decision-support
  dashboard, not a trading terminal.
- No alerting / on-call agent in v1 (rubric: deliberately skipped; the 10-point
  bar is cleared without them).

## Data contract

`openapi.yaml` is the source of truth. Frontend and backend both follow it;
any endpoint change updates the YAML first.

## Public task tracker

GitHub Projects board linked from the repo (created at repo setup): columns
`Backlog / Doing / Done`, one issue per user story with the acceptance criteria
above pasted in. Agent work references the issue number in commit messages.
