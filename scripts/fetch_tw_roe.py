#!/usr/bin/env python3
"""
fetch_tw_roe.py
依公開資訊觀測站財報 (證交所、櫃買中心開放資料) 計算「台股追蹤」各公司的 ROE,並比照美股門檻分 A~D 級。

資料來源 (官方開放資料,免金鑰;只提供「最新一季」的年初累計數):
  - 上市:openapi.twse.com.tw  t187ap06_L_ci (綜合損益表)、t187ap07_L_ci (資產負債表)
  - 上櫃:www.tpex.org.tw openapi mopsfin_t187ap06_O_ci、mopsfin_t187ap07_O_ci

ROE = 歸屬於母公司業主淨利 ÷ 歸屬於母公司業主權益 (期末)
  - 有去年第四季與去年同季累計數時 → 近四季 = 今年累計 + 去年全年 − 去年同季累計
  - 第四季 → 全年
  - 其他 → 年初累計 × 4 / 季數 (年化估算,受淡旺季影響)
每季財報公布後,累計數存入 history,一年後即可改用近四季。

輸出: data/tw_roe.json (財報未變動時不寫檔)
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fetch_tw_prices import ROOT, TZ, WATCHLIST, get_json  # noqa: E402
from fetch_us_prices import ROE_LEVELS  # noqa: E402  (門檻與美股一致)

OUT = ROOT / "data" / "tw_roe.json"
SOURCES = {
    "上市": ("https://openapi.twse.com.tw/v1/opendata/t187ap06_L_ci",
             "https://openapi.twse.com.tw/v1/opendata/t187ap07_L_ci"),
    "上櫃": ("https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap06_O_ci",
             "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap07_O_ci"),
}
NI = "淨利（淨損）歸屬於母公司業主"
EQUITY = "歸屬於母公司業主之權益合計"


def pick(row, *keys):
    return next((row[k] for k in keys if row.get(k) not in (None, "")), None)


def fetch_rows(url):
    """以公司代號索引;櫃買中心檔案較大,偶爾傳輸中斷,重試幾次。"""
    for i in range(4):
        try:
            return {pick(r, "公司代號", "SecuritiesCompanyCode"): r for r in get_json(url)}
        except Exception as e:
            print(f"  ⚠️  {url.rsplit('/', 1)[1]} 第 {i + 1} 次失敗: {e}")
            time.sleep(5)
    raise RuntimeError(f"無法取得 {url}")


def period_of(row):
    return f"{pick(row, '年度', 'Year')}Q{pick(row, '季別', 'Season')}"


def compute(code, hist):
    """由 history 中最新一季計算 ROE。"""
    period = max(hist, key=lambda p: (int(p.split("Q")[0]), int(p.split("Q")[1])))
    year, q = map(int, period.split("Q"))
    cur = hist[period]
    if cur["equity"] is None or cur["ni_ytd"] is None:
        return {"period": period, "roe": None, "roe_basis": "", "level": None}
    prev_fy, prev_same = hist.get(f"{year - 1}Q4"), hist.get(f"{year - 1}Q{q}")
    if q == 4:
        ni, basis = cur["ni_ytd"], "全年"
    elif prev_fy and prev_same:
        ni, basis = cur["ni_ytd"] + prev_fy["ni_ytd"] - prev_same["ni_ytd"], "近四季"
    else:
        ni, basis = cur["ni_ytd"] * 4 / q, "年化"
    if cur["equity"] <= 0:
        return {"period": period, "roe": None, "roe_basis": "股東權益為負", "level": None}
    roe = round(ni / cur["equity"] * 100, 1)
    level = next(lv for lv, floor in ROE_LEVELS if floor is None or roe >= floor)
    return {"period": period, "roe": roe, "roe_basis": basis, "level": level}


def main():
    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    history = old.get("history", {})

    for market, (inc_url, bal_url) in SOURCES.items():
        codes = [c for c, (_, m) in WATCHLIST.items() if m == market]
        try:
            inc, bal = fetch_rows(inc_url), fetch_rows(bal_url)
        except RuntimeError as e:  # 單一市場失敗:沿用上次資料
            print(f"  ❌ {market}: {e}")
            continue
        for code in codes:
            i, b = inc.get(code), bal.get(code)
            if not (i and b) or period_of(i) != period_of(b):
                print(f"  ⚠️  {code} {WATCHLIST[code][0]}: 一般業財報中找不到或期別不一致,略過")
                continue
            to_num = lambda v: float(v) if v not in (None, "") else None
            history.setdefault(code, {})[period_of(i)] = {
                "ni_ytd": to_num(i.get(NI)), "equity": to_num(b.get(EQUITY))}

    stocks = {}
    for code, (name, _) in WATCHLIST.items():
        if history.get(code):
            stocks[code] = {"name": name, **compute(code, history[code])}
            s = stocks[code]
            print(f"  {code} {name:6} {s['period']}  ROE {s['roe']} ({s['roe_basis']}) → {s['level'] or '不分級'}")
        else:
            print(f"  {code} {name:6} 無財報資料")

    if stocks == old.get("stocks") and history == old.get("history") and "--force" not in sys.argv:
        print("ℹ️  財報未變動,不更新檔案")
        return
    periods = sorted({s["period"] for s in stocks.values()})
    OUT.write_text(json.dumps({
        "updated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "period": periods[-1] if periods else "",
        "source": "公開資訊觀測站 (證交所、櫃買中心開放資料)",
        "roe_levels": {lv: floor for lv, floor in ROE_LEVELS},
        "stocks": stocks,
        "history": history,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"✅ 台股 ROE: {len(stocks)}/{len(WATCHLIST)} 檔,最新財報期別 {', '.join(periods)}")


if __name__ == "__main__":
    main()
