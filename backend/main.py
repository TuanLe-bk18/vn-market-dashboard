"""VN Market Dashboard backend.

Serves a bundled market snapshot (data/market_snapshot.json, generated from a
local OHLCV store) and a SQLite-backed dynamic watchlist. The static frontend
is served from ../frontend at /.
"""
import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import db

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "..", "data")
FRONTEND_DIR = os.path.join(BASE, "..", "frontend")
SNAPSHOT_PATH = os.path.join(DATA_DIR, "market_snapshot.json")

app = FastAPI(title="VN Market Dashboard", version="0.1.0")

# Initialize storage at import time so the table exists for tests,
# `uvicorn` workers, and single-command docker runs alike.
db.init_db()


def load_snapshot():
    with open(SNAPSHOT_PATH) as f:
        return json.load(f)


class WatchlistIn(BaseModel):
    code: str = Field(..., min_length=1, max_length=12)
    thesis: str = ""
    resistance: str = ""
    support: str = ""
    invalidate: str = ""
    status: str = "watching"
    notes: str = ""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/market/summary")
def market_summary():
    snap = load_snapshot()
    return {
        "asof": snap["asof"],
        "vnindex": snap["vnindex"],
        "breadth": snap["breadth"],
        "tickers": list(snap["tickers"].keys()),
    }


@app.get("/api/market/tickers/{code}")
def ticker_detail(code: str):
    snap = load_snapshot()
    code = code.upper()
    if code not in snap["tickers"]:
        raise HTTPException(status_code=404, detail=f"ticker {code} not in snapshot")
    return {"code": code, "series": snap["tickers"][code]}


@app.get("/api/watchlist")
def get_watchlist():
    return db.list_entries()


@app.post("/api/watchlist", status_code=201)
def create_watchlist_entry(entry: WatchlistIn):
    return db.add_entry(entry.model_dump())


@app.delete("/api/watchlist/{entry_id}", status_code=204)
def remove_watchlist_entry(entry_id: int):
    if not db.delete_entry(entry_id):
        raise HTTPException(status_code=404, detail="entry not found")
    return None


app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
