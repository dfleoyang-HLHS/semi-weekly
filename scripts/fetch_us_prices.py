#!/usr/bin/env python3
"""
fetch_us_prices.py
美股盤後抓取「美股追蹤」頁面各公司的收盤價與近期漲跌,資料來源 Finnhub (免費方案)。

輸出: data/us_prices.json
  - as_of:     收盤交易日 (美東日期)
  - stocks:    每檔最新報價與報酬 (當日、5 日、月初至今、13 週、年初至今、52 週高低)
  - history:   每檔每日收盤價紀錄 [[日期, 收盤價], ...],每次執行累積一筆

環境變數: FINNHUB_API_KEY (到 https://finnhub.io 免費註冊取得)
"""

import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "us_prices.json"
API = "https://finnhub.io/api/v1"

# 美股追蹤頁面的公司 (代號: 名稱)
WATCHLIST = {
    "NVDA": "NVIDIA", "AVGO": "Broadcom", "AMD": "AMD", "SMCI": "Super Micro",
    "INTC": "Intel", "AMAT": "Applied Materials", "MU": "Micron", "AMKR": "Amkor",
    "DELL": "Dell Technologies", "HPE": "HPE", "AAPL": "Apple", "GOOGL": "Alphabet",
    "META": "Meta", "LRCX": "Lam Research", "MRVL": "Marvell", "TSLA": "Tesla",
}

# Finnhub 基本財務指標欄位 → 輸出欄位 (報酬為 %)
METRIC_FIELDS = {
    "ret_5d": "5DayPriceReturnDaily",
    "ret_mtd": "monthToDatePriceReturnDaily",
    "ret_13w": "13WeekPriceReturnDaily",
    "ret_ytd": "yearToDatePriceReturnDaily",
    "high_52w": "52WeekHigh",
    "low_52w": "52WeekLow",
    "market_cap_m": "marketCapitalization",  # 百萬美元
}

ET = timezone(timedelta(hours=-4))  # 美東 (夏令);僅用於把報價時間換成交易日期


def get(path, key, **params):
    url = f"{API}/{path}?{urllib.parse.urlencode({**params, 'token': key})}"
    req = urllib.request.Request(url, headers={"User-Agent": "semi-weekly/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def num(v, nd=2):
    return round(float(v), nd) if isinstance(v, (int, float)) else None


def fetch_symbol(symbol, key):
    q = get("quote", key, symbol=symbol)
    if not q or not q.get("c"):
        raise ValueError(f"{symbol} 沒有報價資料: {q}")
    m = get("stock/metric", key, symbol=symbol, metric="all").get("metric", {}) or {}
    trade_date = datetime.fromtimestamp(q["t"], ET).date().isoformat() if q.get("t") else ""
    row = {
        "name": WATCHLIST[symbol],
        "price": num(q["c"]), "change": num(q.get("d")), "change_pct": num(q.get("dp")),
        "prev_close": num(q.get("pc")), "open": num(q.get("o")),
        "high": num(q.get("h")), "low": num(q.get("l")),
        "trade_date": trade_date,
    }
    for out, field in METRIC_FIELDS.items():
        row[out] = num(m.get(field))
    return row


def main():
    key = os.environ.get("FINNHUB_API_KEY")
    if not key:
        sys.exit("請設定環境變數 FINNHUB_API_KEY (GitHub: Settings → Secrets → Actions)")

    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    stocks, history, failed = {}, old.get("history", {}), []

    for i, symbol in enumerate(WATCHLIST):
        try:
            stocks[symbol] = fetch_symbol(symbol, key)
            s = stocks[symbol]
            print(f"  {symbol:6} {s['price']:>10}  {s['change_pct']:+.2f}%  ({s['trade_date']})")
        except Exception as e:  # 單檔失敗不影響其他檔;沿用上次資料
            failed.append(symbol)
            print(f"  ❌ {symbol}: {e}")
            if symbol in old.get("stocks", {}):
                stocks[symbol] = {**old["stocks"][symbol], "stale": True}
        if i < len(WATCHLIST) - 1:
            time.sleep(1.1)  # 免費方案每分鐘 60 次,每檔 2 次請求

    # 累積每日收盤價 (同一交易日重複執行只保留一筆)
    for symbol, s in stocks.items():
        if s.get("stale") or not s.get("trade_date"):
            continue
        rows = [r for r in history.get(symbol, []) if r[0] != s["trade_date"]]
        history[symbol] = sorted(rows + [[s["trade_date"], s["price"]]])

    dates = [s["trade_date"] for s in stocks.values() if s.get("trade_date") and not s.get("stale")]
    if not dates:
        sys.exit("❌ 所有股票都抓取失敗,不更新檔案")

    # 非交易日 (美國國定假日等):最新交易日與上次相同,不寫檔、不 commit、不部署
    new_symbols = set(stocks) - set(old.get("stocks", {}))  # 新加入追蹤的股票要立即寫入
    if max(dates) == old.get("as_of") and not new_symbols and "--force" not in sys.argv:
        print(f"ℹ️  最新交易日仍為 {max(dates)},今日非交易日或資料未更新,略過")
        return

    OUT.write_text(json.dumps({
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "as_of": max(dates),
        "source": "Finnhub",
        "stocks": stocks,
        "history": history,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"✅ 美股報價: {len(WATCHLIST) - len(failed)}/{len(WATCHLIST)} 檔成功,交易日 {max(dates)}")
    if failed:
        print(f"   ⚠️  失敗 (沿用上次資料): {', '.join(failed)}")


if __name__ == "__main__":
    main()
