#!/usr/bin/env python3
"""
update_tw_cards.py
每日 15:00 (台灣時間) 更新「台股追蹤」卡片的指標、近期重點與標籤 (data/tw_stocks.json)。

流程:
  1. 從新聞資料庫取出「上次檢查之後」新收錄的新聞 (以 archive id 記錄,不重複處理)
  2. 只挑出提到追蹤公司的新聞;沒有就結束 (不呼叫 Claude、不改檔)
  3. Claude 依新聞更新有新資訊的公司 (與週報相同的卡片規則)
  4. Claude 獨立事實查核:有問題的公司還原為原卡片,其餘直接發佈
輸出:GITHUB_OUTPUT changed=true|false

用法: python scripts/update_tw_cards.py [--dry-run]
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from archive_news import load_archive  # noqa: E402
from generate_news_brief import keyword_in  # noqa: E402

ROOT = Path(__file__).parent.parent
CARDS = ROOT / "data" / "tw_stocks.json"
PRICES = ROOT / "data" / "tw_prices.json"
TZ = timezone(timedelta(hours=8))
LOOKBACK_DAYS = 3  # 第一次執行 (沒有檢查紀錄) 時往回看的天數

# 新聞中常見的公司寫法 (中文簡稱、俗稱、英文名稱);英文以完整單字比對
ALIASES = {
    "2330": ["台積電", "台積", "TSMC"], "2303": ["聯電", "UMC"], "3711": ["日月光", "ASE Technology", "ASEH"],
    "6239": ["力成", "Powertech"], "2449": ["京元電", "KYEC"], "2454": ["聯發科", "MediaTek"],
    "3661": ["世芯", "Alchip"], "3443": ["創意電子", "GUC", "Global Unichip"], "8299": ["群聯", "Phison"],
    "2408": ["南亞科", "Nanya"], "3037": ["欣興", "Unimicron"], "2308": ["台達電", "Delta Electronics"],
    "2317": ["鴻海", "Foxconn", "Hon Hai"], "2382": ["廣達", "Quanta"], "3231": ["緯創", "Wistron"],
    "6669": ["緯穎", "Wiwynn"], "4938": ["和碩", "Pegatron"], "2357": ["華碩", "ASUS"],
    "2344": ["華邦電", "華邦", "Winbond"], "4979": ["華星光", "LuxNet"], "8021": ["尖點", "Topoint"],
    "2353": ["宏碁", "Acer"],
}

FACT_SYSTEM = """你是嚴格的財經事實查核員。你會拿到「新聞清單」(唯一的事實依據)、每家公司「更新前的卡片」與「更新後的卡片」。
只查核更新後卡片中「新增或改寫」的內容 (與更新前相同的內容不需查核):
- 具體數字、金額、百分比、日期、排名與事件,必須能在新聞清單的標題或摘要中找到依據;合理換算、四捨五入、單位轉換可接受
- 沒有依據、與新聞矛盾、把傳聞寫成確定、或把其他公司的消息寫到這家公司的,列入 issues
- where 請填公司代號 (ticker)
- 不要評論文筆,只看事實
沒有問題時 issues 回傳空陣列。"""


def relevant_news(cards, since_id):
    """回傳 ({代號: [新聞]}, 合併後的新聞清單, 本次看到的最大 archive id)"""
    archive = load_archive()
    if since_id is None:
        start = (datetime.now(TZ).date() - timedelta(days=LOOKBACK_DAYS)).isoformat()
        new = [a for a in archive if a["published"] >= start]
    else:
        new = [a for a in archive if a["id"] > since_id]
    max_id = max([a["id"] for a in archive] + [since_id or 0])
    by_code, picked = {}, {}
    for a in new:
        text = f"{a['title']} {a['summary']}"
        for c in cards:
            names = ALIASES.get(c["ticker"], []) + [c["name"]]
            if any(keyword_in(n, text) for n in names):
                by_code.setdefault(c["ticker"], []).append(a)
                picked[a["id"]] = a
    items = [{"title": a["title"], "link": a["url"], "source": a["source"], "published": a["published"],
              "summary": a["summary"], "archive_id": a["id"]}
             for a in sorted(picked.values(), key=lambda x: (x["published"], x["id"]), reverse=True)]
    return by_code, items, max_id


def fact_check(client, items, before, after):
    from generate_draft import build_news_block, call_claude
    from verify_weekly import FACT_SCHEMA
    content = [{"ticker": t, "name": after[t]["name"],
                "更新前": {"metrics": before[t]["metrics"], "news": before[t]["news"]},
                "更新後": {"metrics": after[t]["metrics"], "news": after[t]["news"]}} for t in after]
    return json.loads(call_claude(
        client, FACT_SYSTEM,
        f"【新聞清單】\n{build_news_block(items)}\n\n【待查核卡片】\n{json.dumps(content, ensure_ascii=False, indent=1)}",
        output_config={"format": {"type": "json_schema", "schema": FACT_SCHEMA}},
    ))


def set_output(changed):
    if gh := os.environ.get("GITHUB_OUTPUT"):
        with open(gh, "a", encoding="utf-8") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")


def main():
    data = json.loads(CARDS.read_text(encoding="utf-8"))
    by_code, items, max_id = relevant_news(data["stocks"], data.get("news_checked_id"))
    print(f"📰 新收錄新聞中提到追蹤公司:{len(items)} 則,{len(by_code)} 家 "
          f"({', '.join(f'{c}×{len(v)}' for c, v in by_code.items())})")
    if not by_code or "--dry-run" in sys.argv:
        set_output(False)
        return
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("請設定環境變數 ANTHROPIC_API_KEY")

    import anthropic
    from generate_draft import update_stock_cards
    client = anthropic.Anthropic()
    today = datetime.now(TZ).date().isoformat()
    before = {c["ticker"]: json.loads(json.dumps(c)) for c in data["stocks"]}
    updated = update_stock_cards(client, None, items, today, CARDS, PRICES, "台股追蹤",
                                 period="今日", only=set(by_code))

    data = json.loads(CARDS.read_text(encoding="utf-8"))
    if updated:
        after = {c["ticker"]: c for c in data["stocks"] if c["ticker"] in updated}
        try:
            result = fact_check(client, items, before, after)
            issues = result["issues"]
        except Exception as e:  # 查核失敗時一律不發佈這次的更新
            print(f"   ⚠️  事實查核失敗,全部還原: {e}")
            issues = [{"where": t, "claim": "", "problem": "查核程式失敗"} for t in updated]
        bad = {t for t in updated for i in issues if t in i["where"] or after[t]["name"] in i["where"]}
        for i in issues:
            print(f"   ✗ {i['where']}: {i['claim']} → {i['problem']}")
        data["stocks"] = [before[c["ticker"]] if c["ticker"] in bad else c for c in data["stocks"]]
        updated = [t for t in updated if t not in bad]
        print(f"✅ 通過查核並更新:{updated or '無'};還原:{sorted(bad) or '無'}")
    data["news_checked_id"] = max_id
    CARDS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    set_output(True)  # 至少檢查紀錄有更新;實際內容是否變動由 git diff 判斷


if __name__ == "__main__":
    main()
