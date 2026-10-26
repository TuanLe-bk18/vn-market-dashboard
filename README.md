# VN Market Dashboard

Live app: [https://vn-market-dashboard-91zt.onrender.com](https://vn-market-dashboard-91zt.onrender.com/)

Project board: [https://github.com/users/TuanLe-bk18/projects/1)](https://github.com/users/TuanLe-bk18/projects/1)

A full-stack web app that turns a daily Vietnam-stock-market data pipeline into an
actionable dashboard: market breadth snapshot (VNINDEX, B20/B50/B200 breadth,
B200<30 fuse) plus a dynamic watchlist with per-ticker thesis, resistance /
support levels, and invalidation conditions.

Built for **DataTalksClub AI Dev Tools Zoomcamp 2026 — Project 1**.

## Problem

A retail investor running a rules-based strategy on the Vietnamese market checks
the same three things every session: (1) is the market in a state where the
strategy may open positions, (2) what are the levels on the handful of tickers
being watched, (3) did any thesis break and need a rewrite. Today that lives in
scattered chat messages and a hand-edited markdown table — levels go stale,
broken theses linger, and there is no single place to see "market state +
my levels" before the session starts.

## What the system does

- **Market snapshot** (`GET /api/market/summary`): VNINDEX close and day change,
  breadth (% of liquid tickers above SMA20/50/200), and the B200<30 "fuse" that
  blocks bull-style entries. Data is bundled as `data/market_snapshot.json`,
  generated from the local OHLCV store by `build_snapshot.py`.
- **Ticker detail** (`GET /api/market/tickers/{code}`): last 60 sessions of
  OHLC + volume + SMA20/50 for watched tickers.
- **Dynamic watchlist** (`GET/POST/DELETE /api/watchlist`): each entry carries a
  thesis, resistance, support, and an explicit invalidation condition — the
  "rewrite the thesis when the level breaks" discipline, enforced by schema
  instead of memory.
- **Single-page frontend** (no build step): KPI cards, ticker table, watchlist
  table with add/delete.

## Run it (one command)

```bash
docker compose up --build
# open http://localhost:8000
```

Local dev without Docker:

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
pytest -q   # tests, one command
```

## Refresh the market snapshot

```bash
python build_snapshot.py   # regenerates data/market_snapshot.json from the local store
```

The public deployment serves the bundled snapshot; it never depends on the
local cron pipeline.

## Repo layout

```
product-spec.md        product spec (user stories, acceptance criteria, non-goals)
AGENTS.md              working agreement for humans and AI agents
openapi.yaml           API contract (source of truth for frontend + backend)
backend/               FastAPI app + SQLite watchlist storage
frontend/              single-page app (vanilla JS, no build step)
data/                  bundled market_snapshot.json + seed_watchlist.json
tests/                 pytest suite (runs with one command)
docs/                  agent-team.md, ai-usage-report.md
Dockerfile / docker-compose.yml / render.yaml
.github/workflows/ci.yml
```

## Privacy note

This repo is public for peer review. The seed watchlist contains **public market
levels only** — never commit real position sizes or account data. The SQLite DB
(`*.db`) is git-ignored; entries you add locally stay local.
