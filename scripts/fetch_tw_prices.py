#!/usr/bin/env python3
"""
fetch_tw_prices.py
台股盤後抓取「台股追蹤」頁面各公司的收盤價,並由累積的每日收盤價計算近期漲跌。

資料來源 (官方開放資料,免金鑰):
  - 證交所 (上市):openapi.twse.com.tw  STOCK_DAY_ALL;歷史:www.twse.com.tw STOCK_DAY
  - 櫃買中心 (上櫃):www.tpex.org.tw openapi 每日收盤行情;歷史:個股日成交資訊

輸出: data/tw_prices.json
  - as_of:   最新交易日
  - stocks:  每檔收盤價、當日漲跌、5 日 / 本月 / 13 週 / 今年報酬、52 週高低
             (已還原除權 / 分割;現金除息未還原)
  - history: 每檔每日收盤價 [[日期, 收盤價], ...]

用法:
  python scripts/fetch_tw_prices.py                    # 抓最新一個交易日 (每日排程)
  python scripts/fetch_tw_prices.py --backfill 13      # 補建最近 13 個月的歷史收盤價 (首次使用)
  python scripts/fetch_tw_prices.py --backfill 13 --only 4979,8021   # 只補建指定代號 (新增公司時)
"""

import json
import ssl
import sys
import time
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "tw_prices.json"
TZ = timezone(timedelta(hours=8))

# 台股追蹤頁面的公司 (代號: (名稱, 市場))
WATCHLIST = {
    "2330": ("台積電", "上市"), "2303": ("聯電", "上市"),
    "3711": ("日月光投控", "上市"), "6239": ("力成", "上市"), "2449": ("京元電子", "上市"),
    "2454": ("聯發科", "上市"), "3661": ("世芯-KY", "上市"), "3443": ("創意", "上市"), "8299": ("群聯", "上櫃"),
    "2408": ("南亞科", "上市"),
    "3037": ("欣興", "上市"), "2308": ("台達電", "上市"),
    "2317": ("鴻海", "上市"), "2382": ("廣達", "上市"), "3231": ("緯創", "上市"),
    "6669": ("緯穎", "上市"), "4938": ("和碩", "上市"), "2357": ("華碩", "上市"),
    "2344": ("華邦電", "上市"), "4979": ("華星光", "上櫃"), "8021": ("尖點", "上市"), "2353": ("宏碁", "上市"),
}

TWSE_DAILY = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
TPEX_DAILY = "https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes"
TWSE_MONTH = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date={d}&stockNo={code}&response=json"
TPEX_MONTH = "https://www.tpex.org.tw/www/zh-tw/afterTrading/tradingStock?code={code}&date={d}&response=json"
# 當日行情 (網站版):收盤後約 14:00 起公布;開放資料 API (上面兩個 DAILY) 要到傍晚才更新
TWSE_TODAY = "https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date={d}&type=ALLBUT0999&response=json"
TPEX_TODAY = "https://www.tpex.org.tw/www/zh-tw/afterTrading/otc?date={d}&type=EW&response=json"


# 證交所憑證缺少 Subject Key Identifier,Python 3.13+ 預設的 X.509 嚴格模式會拒絕;
# 僅關閉嚴格模式這項額外檢查,憑證鏈與主機名稱驗證仍保留
SSL_CTX = ssl.create_default_context()
SSL_CTX.verify_flags &= ~getattr(ssl, "VERIFY_X509_STRICT", 0)


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (semi-weekly)"})
    with urllib.request.urlopen(req, timeout=60, context=SSL_CTX) as resp:
        return json.load(resp)


def roc_to_iso(s):
    """民國日期 '1150930' 或 '115/09/30' → '2026-09-30'"""
    s = s.replace("/", "")
    return date(int(s[:-4]) + 1911, int(s[-4:-2]), int(s[-2:])).isoformat()


def to_float(s):
    try:
        return float(str(s).replace(",", "").replace("+", ""))
    except ValueError:
        return None  # 無成交為 "--"


def fetch_latest():
    """抓最新交易日收盤價:回傳 {代號: (日期, 收盤價)}"""
    out = {}
    for row in get_json(TWSE_DAILY):
        if row.get("Code") in WATCHLIST and (c := to_float(row.get("ClosingPrice"))):
            out[row["Code"]] = (roc_to_iso(row["Date"]), c)
    for row in get_json(TPEX_DAILY):
        code = row.get("SecuritiesCompanyCode")
        if code in WATCHLIST and (c := to_float(row.get("Close"))):
            out[code] = (roc_to_iso(row["Date"]), c)
    return out


def fetch_today(day):
    """抓指定日期的當日收盤 (證交所每日收盤行情、櫃買中心上櫃股票行情):回傳 {代號: (日期, 收盤價)}。
    尚未公布或休市時回傳空的 (或只有其中一個市場)。"""
    out = {}
    try:
        data = get_json(TWSE_TODAY.format(d=day.strftime("%Y%m%d")))
        for t in data.get("tables", []) if data.get("stat") == "OK" else []:
            f = t.get("fields") or []
            if "證券代號" in f and "收盤價" in f:
                ci, pi = f.index("證券代號"), f.index("收盤價")
                for r in t.get("data", []):
                    if r[ci] in WATCHLIST and (c := to_float(r[pi])):
                        out[r[ci]] = (day.isoformat(), c)
    except Exception as e:
        print(f"  ⚠️  證交所當日行情抓取失敗: {e}", flush=True)
    try:
        data = get_json(TPEX_TODAY.format(d=day.strftime("%Y/%m/%d")))
        for t in data.get("tables", []):
            if not t.get("date") or roc_to_iso(t["date"]) != day.isoformat():
                continue  # 尚未公布時會回傳前一交易日,不採用
            f = [x.strip() for x in t.get("fields") or []]
            if "代號" in f and "收盤" in f:
                ci, pi = f.index("代號"), f.index("收盤")
                for r in t.get("data", []):
                    if r[ci] in WATCHLIST and (c := to_float(r[pi])):
                        out[r[ci]] = (day.isoformat(), c)
    except Exception as e:
        print(f"  ⚠️  櫃買中心當日行情抓取失敗: {e}", flush=True)
    return out


def fetch_month(code, market, first_day):
    """抓單一個股某月份的每日收盤價:回傳 [(日期, 收盤價), ...]"""
    if market == "上市":
        data = get_json(TWSE_MONTH.format(d=first_day.strftime("%Y%m%d"), code=code))
        rows = data.get("data", []) if data.get("stat") == "OK" else []
    else:
        data = get_json(TPEX_MONTH.format(d=first_day.strftime("%Y%%2F%m%%2F%d"), code=code))
        rows = (data.get("tables") or [{}])[0].get("data", [])
    return [(roc_to_iso(r[0]), c) for r in rows if (c := to_float(r[6]))]


def add_history(history, code, rows):
    merged = dict(map(tuple, history.get(code, [])))
    merged.update(rows)
    history[code] = sorted([d, p] for d, p in merged.items())


LIMIT = 0.105  # 台股漲跌幅限制 10%;單日變動超過此值必為除權、分割或減資


def adjust_splits(rows):
    """還原除權 / 分割 / 減資:單日變動超過漲跌幅限制時,將之前的價格等比例調整。
    回傳 (調整後 rows, 偵測到的事件)。現金除息缺口小於 10%,無法以此偵測。"""
    adj = [list(r) for r in rows]
    events = []
    for i in range(len(adj) - 1, 0, -1):
        prev, cur = rows[i - 1][1], rows[i][1]
        ratio = cur / prev
        if abs(ratio - 1) > LIMIT:
            events.append((rows[i][0], round(ratio, 4)))
            for j in range(i):
                adj[j][1] = adj[j][1] * ratio
    return [tuple(r) for r in adj], events


def compute(code, rows):
    """由每日收盤價計算當日漲跌與各期間報酬 (%);報酬與 52 週區間使用還原除權 / 分割後的價格"""
    if not rows:
        return None
    rows, events = adjust_splits(rows)
    closes = [p for _, p in rows]
    last_date, price = rows[-1]
    d = date.fromisoformat(last_date)

    def pct(base):
        return round((price / base - 1) * 100, 2) if base else None

    def close_before(day):  # 指定日期之前最後一個收盤價
        prior = [p for t, p in rows if t < day]
        return prior[-1] if prior else None

    year_ago = (d - timedelta(days=365)).isoformat()
    window = [p for t, p in rows if t > year_ago]
    prev = closes[-2] if len(closes) > 1 else None
    name, market = WATCHLIST[code]
    return {
        "name": name, "market": market, "trade_date": last_date, "price": price,
        "change": round(price - prev, 2) if prev else None, "change_pct": pct(prev),
        "ret_5d": pct(closes[-6]) if len(closes) > 5 else None,
        "ret_mtd": pct(close_before(d.replace(day=1).isoformat())),
        "ret_13w": pct(closes[-66]) if len(closes) > 65 else None,
        "ret_ytd": pct(close_before(f"{d.year}-01-01")),
        "high_52w": round(max(window), 2), "low_52w": round(min(window), 2),
        **({"adjusted": [f"{d} ×{r}" for d, r in events]} if events else {}),
    }


def main():
    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    history = old.get("history", {})

    if "--backfill" in sys.argv:
        months = int(sys.argv[sys.argv.index("--backfill") + 1])
        today = datetime.now(TZ).date()
        firsts = []
        y, m = today.year, today.month
        for _ in range(months):
            firsts.append(date(y, m, 1))
            y, m = (y, m - 1) if m > 1 else (y - 1, 12)
        only = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
        for code, (name, market) in WATCHLIST.items():
            if only and code not in only:
                continue
            got = 0
            for first in reversed(firsts):
                try:
                    rows = fetch_month(code, market, first)
                    add_history(history, code, rows)
                    got += len(rows)
                except Exception as e:
                    print(f"  ⚠️  {code} {name} {first:%Y-%m}: {e}", flush=True)
                time.sleep(3.5)  # 證交所限制請求頻率 (約每 5 秒 3 次)
            print(f"  {code} {name}: 補建 {got} 個交易日", flush=True)

    try:
        latest = fetch_latest()
    except Exception as e:  # 最新收盤抓取失敗時,仍保留已補建的歷史 (不讓補建白做)
        print(f"  ⚠️  最新收盤抓取失敗,僅使用歷史資料:{e}", flush=True)
        latest = {}
    # 當日行情比開放資料 API 早公布;較新的日期優先
    for code, (d, c) in fetch_today(datetime.now(TZ).date()).items():
        if code not in latest or d > latest[code][0]:
            latest[code] = (d, c)
    for code, (d, c) in latest.items():
        add_history(history, code, [(d, c)])
    # 月資料 API 有時比每日 API 早公布當天收盤;以每日 API 的最新日期為準,避免各檔日期不一致
    if latest:
        cutoff = max(d for d, _ in latest.values())
        for code in history:
            history[code] = [r for r in history[code] if r[0] <= cutoff]
    missing = [c for c in WATCHLIST if c not in latest]

    stocks = {code: s for code in WATCHLIST if (s := compute(code, history.get(code, [])))}
    if not stocks:
        sys.exit("❌ 沒有任何台股資料,不更新檔案")
    as_of = max(s["trade_date"] for s in stocks.values())
    for code, s in stocks.items():
        if s["trade_date"] != as_of:
            s["stale"] = True

    # 非交易日 (國定假日、颱風假等):最新交易日與上次相同,不寫檔、不 commit、不部署
    # 同一交易日再次執行時 (例如 14:00 上櫃尚未公布、16:00 補抓),有原本「未更新」的個股補上才寫檔
    old_stale = {c for c, s in old.get("stocks", {}).items() if s.get("stale")}
    filled = old_stale - {c for c, s in stocks.items() if s.get("stale")}
    if as_of == old.get("as_of") and not filled and "--backfill" not in sys.argv and "--force" not in sys.argv:
        print(f"ℹ️  最新交易日仍為 {as_of},今日非交易日或資料未更新,略過")
        return

    OUT.write_text(json.dumps({
        "updated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "as_of": as_of,
        "source": "臺灣證券交易所、證券櫃檯買賣中心",
        "stocks": stocks,
        "history": history,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for code, s in stocks.items():
        print(f"  {code} {s['name']:6} {s['price']:>9}  {s['change_pct'] if s['change_pct'] is not None else '–':>6}%  今年 {s['ret_ytd']}%")
    print(f"✅ 台股報價: {len(WATCHLIST) - len(missing)}/{len(WATCHLIST)} 檔取得最新收盤,交易日 {as_of}")
    if missing:
        print(f"   ⚠️  未取得最新收盤 (沿用歷史): {', '.join(missing)}")


if __name__ == "__main__":
    main()
