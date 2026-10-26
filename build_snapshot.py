"""Build data/market_snapshot.json for the Project 1 scaffold from the local store.

Reads /home/hatch/market/store/bars/*.json (as of last close 2026-10-22),
computes breadth B20/B50/B200, VNINDEX series, and OHLC+SMA series for
watchlist codes. Pure read-only w.r.t. the pipeline; writes only the scaffold
snapshot file.
"""
import json, glob, os
import numpy as np
from datetime import datetime, timezone

STORE = "/home/hatch/market/store/bars"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "market_snapshot.json")
WATCH = ["VIC", "DRI", "PVD"]


def load(code):
    if code == "VNINDEX":
        path = "/home/hatch/market/store/vnindex.json"
    else:
        path = os.path.join(STORE, code + ".json")
    with open(path) as f:
        return json.load(f)


def closes(bars):
    return np.array([b["c"] for b in bars], dtype=float)


def sma(arr, n):
    out = np.full_like(arr, np.nan)
    if len(arr) >= n:
        out[n - 1:] = np.convolve(arr, np.ones(n) / n, mode="valid")
    return out


def liquid(bars):
    """LIQ screener rule (2026-10-01): price 2k-500k VND, VOL MA20 50k-200M shares."""
    if len(bars) < 200:
        return False
    last = bars[-1]
    if not (2000 <= last["c"] <= 500000):
        return False
    vols = [b.get("v") or 0 for b in bars[-20:]]
    ma20 = sum(vols) / 20
    return 50000 <= ma20 <= 200_000_000


def breadth():
    b20 = b50 = b200 = n = 0
    for path in glob.glob(os.path.join(STORE, "*.json")):
        try:
            bars = json.load(open(path))
        except Exception:
            continue
        if not liquid(bars):
            continue
        c = closes(bars)
        n += 1
        if c[-1] > sma(c, 20)[-1]:
            b20 += 1
        if c[-1] > sma(c, 50)[-1]:
            b50 += 1
        if c[-1] > sma(c, 200)[-1]:
            b200 += 1
    return {
        "B20": round(100 * b20 / n, 1) if n else None,
        "B50": round(100 * b50 / n, 1) if n else None,
        "B200": round(100 * b200 / n, 1) if n else None,
        "universe_n": n,
        "universe": "LIQ screener (price 2k-500k VND, VOL MA20 50k-200M shares)",
    }


def series(code, n=60):
    bars = load(code)[-n:]
    c = closes(bars)
    s20, s50 = sma(c, 20), sma(c, 50)
    out = []
    for i, b in enumerate(bars):
        d = datetime.fromtimestamp(b["date"], tz=timezone.utc).strftime("%Y-%m-%d")
        out.append({
            "date": d, "o": b["o"], "h": b["h"], "l": b["l"], "c": b["c"],
            "v": b.get("v"),
            "sma20": None if np.isnan(s20[i]) else round(float(s20[i]), 1),
            "sma50": None if np.isnan(s50[i]) else round(float(s50[i]), 1),
        })
    return out


def main():
    vn_bars = load("VNINDEX")
    vn_c = closes(vn_bars)
    last, prev = vn_c[-1], vn_c[-2]
    snap = {
        "asof": datetime.fromtimestamp(vn_bars[-1]["date"], tz=timezone.utc).strftime("%Y-%m-%d"),
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "local store /home/hatch/market/store (Simplize OHLCV via relay); breadth = % of listed tickers with close > SMA over full store universe",
        "vnindex": {
            "close": round(float(last), 2),
            "change_pct": round(100 * (last - prev) / prev, 2),
            "series": [
                {"date": datetime.fromtimestamp(b["date"], tz=timezone.utc).strftime("%Y-%m-%d"),
                 "c": round(float(b["c"]), 2)}
                for b in vn_bars[-60:]
            ],
        },
        "breadth": breadth(),
        "tickers": {code: series(code) for code in WATCH},
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(snap, f, ensure_ascii=False)
    print("wrote", OUT, "asof", snap["asof"], "breadth", snap["breadth"])


if __name__ == "__main__":
    main()
