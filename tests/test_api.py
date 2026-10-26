"""API tests: run with `pytest` from the repo root (one command)."""
import os
import tempfile

import pytest
from fastapi.testclient import TestClient

# Isolate the watchlist DB per test session: point at a temp file BEFORE app import.
_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp.close()
os.environ["WATCHLIST_DB"] = _tmp.name

from backend.main import app  # noqa: E402

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_market_summary_shape():
    r = client.get("/api/market/summary")
    assert r.status_code == 200
    d = r.json()
    assert "asof" in d and "vnindex" in d and "breadth" in d
    assert d["breadth"]["B200"] is not None
    assert isinstance(d["vnindex"]["close"], (int, float))


def test_ticker_detail():
    r = client.get("/api/market/tickers/VIC")
    assert r.status_code == 200
    d = r.json()
    assert d["code"] == "VIC"
    assert len(d["series"]) > 0
    assert "sma20" in d["series"][-1]


def test_ticker_unknown_404():
    r = client.get("/api/market/tickers/NOPE")
    assert r.status_code == 404


def test_watchlist_crud():
    # seeded entries exist
    r = client.get("/api/watchlist")
    assert r.status_code == 200
    before = len(r.json())
    assert before >= 1

    # create
    r = client.post("/api/watchlist", json={
        "code": "tcb",
        "thesis": "test entry",
        "resistance": "1",
        "support": "2",
        "invalidate": "3",
    })
    assert r.status_code == 201
    created = r.json()
    assert created["code"] == "TCB"  # normalized to upper case
    assert created["id"]

    # list grows
    r = client.get("/api/watchlist")
    assert len(r.json()) == before + 1

    # delete
    r = client.delete(f"/api/watchlist/{created['id']}")
    assert r.status_code == 204
    r = client.get("/api/watchlist")
    assert len(r.json()) == before

    # delete missing -> 404
    r = client.delete("/api/watchlist/999999")
    assert r.status_code == 404


def test_watchlist_requires_code():
    r = client.post("/api/watchlist", json={"thesis": "no code"})
    assert r.status_code == 422
