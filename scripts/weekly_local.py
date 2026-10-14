#!/usr/bin/env python3
"""
weekly_local.py
本機排程 (Claude 訂閱額度、不使用 API) 產生週報的輔助程式。寫作由本機 Claude 完成,本程式負責準備資料與組裝、檢查。

  1. python scripts/weekly_local.py prepare <工作資料夾>
     → week.json (週次 / 日期)、news.txt (編號新聞清單,與 generate_draft.py 相同的 250 則)、items.json、
       prev_supplychain.json (上一期圖)、us_cards.json (目前美股卡片)
  2. 本機 Claude 依 generate_draft.py 的 WEEKLY_SYSTEM / SUPPLYCHAIN_SYSTEM / STOCK_CARDS_SYSTEM 規則撰寫:
       post_body.md      週報 (含 front matter,最後一行為「## 資料來源」標題,來源清單由本程式產生)
       graph.json        {"title","summary","highlights","nodes":[{id,tier,label,sub,region,news_ref}],"edges":[...],"analysis":{...}}
       us_updates.json   {"updates":[{"ticker","metrics":{label: value} 或 null (沿用),"news":[...],"tags":[...] 或省略}]}
  3. python scripts/weekly_local.py finalize <工作資料夾>
     → posts/YYYY-WNN-semi-weekly.md、data/supplychain-YYYY-WNN.json、data/us_stocks.json,
       並執行 verify_weekly 的格式與連結檢查;全部通過時結尾印出 PASSED
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from archive_news import add_mentions, normalize_url, week_news  # noqa: E402
from generate_draft import (DATA_DIR, MAX_NEWS, POSTS_DIR, TZ, US_STOCKS, attach_news,  # noqa: E402
                            build_news_block, latest_supplychain, validate_graph)

SOURCE_NAMES = {"鉅亨網 台股": "鉅亨網", "鉅亨網 美股": "鉅亨網", "TechNews 科技新報": "TechNews", "DigiTimes 中文": "DigiTimes"}


def prepare(work):
    work.mkdir(parents=True, exist_ok=True)
    today = datetime.now(TZ).date()
    year, week, _ = today.isocalendar()
    tag = f"{year}-W{week:02d}"
    items = week_news(7, today)
    if not items:
        sys.exit("⚠️  新聞資料庫過去 7 天沒有新聞")
    prev = latest_supplychain(tag)
    (work / "week.json").write_text(json.dumps({"week": tag, "date": today.isoformat(), "news": min(len(items), MAX_NEWS),
                                                "prev_week": prev["week"] if prev else None}, ensure_ascii=False), encoding="utf-8")
    (work / "items.json").write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
    (work / "news.txt").write_text(build_news_block(items), encoding="utf-8")
    (work / "prev_supplychain.json").write_text(json.dumps(prev, ensure_ascii=False, indent=1), encoding="utf-8")
    (work / "us_cards.json").write_text(US_STOCKS.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"✅ {tag} ({today}):新聞 {len(items)} 則 (使用最新 {min(len(items), MAX_NEWS)} 則),上一期 {prev['week'] if prev else '無'}")
    print(f"   工作資料夾:{work}")


def finalize(work):
    meta = json.loads((work / "week.json").read_text(encoding="utf-8"))
    tag, day = meta["week"], meta["date"]
    items = json.loads((work / "items.json").read_text(encoding="utf-8"))
    errors = []

    # 1. 週報:依內文引用的 [n] 產生資料來源清單
    body = (work / "post_body.md").read_text(encoding="utf-8").rstrip()
    if not body.endswith("## 資料來源"):
        body += "\n\n---\n\n## 資料來源"
    refs = sorted({int(n) for n in re.findall(r"\[(\d+)\]", body.split("## 資料來源")[0])})
    bad = [n for n in refs if not 1 <= n <= min(len(items), MAX_NEWS)]
    if bad:
        errors.append(f"週報引用了不存在的新聞編號:{bad}")
    refs = [n for n in refs if n not in bad]
    lines = [f"- [{n}] [{items[n - 1]['title'].replace('[', '(').replace(']', ')')}]({items[n - 1]['link']}) — "
             f"{SOURCE_NAMES.get(items[n - 1]['source'], items[n - 1]['source'])}" for n in refs]
    post = body + "\n\n" + "\n".join(lines) + "\n"
    post_path = POSTS_DIR / f"{tag}-semi-weekly.md"
    post_path.write_text(post, encoding="utf-8")
    print(f"📝 {post_path.name}:{len(post)} 字元,引用 {len(refs)} 則新聞")

    # 2. 供應鏈圖:news_ref → 新聞連結、近 4 週報導量
    graph = json.loads((work / "graph.json").read_text(encoding="utf-8"))
    prev = latest_supplychain(tag)
    graph = attach_news(validate_graph(graph), items, prev)
    graph = {"week": tag, "date": day, **graph}
    add_mentions(graph, day)
    sc_path = DATA_DIR / f"supplychain-{tag}.json"
    sc_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"🔗 {sc_path.name}:{len(graph['nodes'])} 節點 / {len(graph['edges'])} 關係")

    # 3. 美股卡片
    upd_path = work / "us_updates.json"
    if upd_path.exists():
        d = json.loads(US_STOCKS.read_text(encoding="utf-8"))
        cards = {c["ticker"]: c for c in d["stocks"]}
        done = []
        for u in json.loads(upd_path.read_text(encoding="utf-8")).get("updates", []):
            c = cards.get(u.get("ticker"))
            news = [n.strip() for n in u.get("news", []) if n.strip()][:4]
            if not c:
                errors.append(f"美股卡片 {u.get('ticker')} 不存在")
                continue
            if len(news) < 2:
                errors.append(f"美股卡片 {c['ticker']} 近期重點少於 2 條")
                continue
            if u.get("metrics"):
                m = {(k + " 年" if k.strip().isdigit() else k.strip()): str(v).strip() for k, v in u["metrics"].items()}
                if not 2 <= len(m) <= 4:
                    errors.append(f"美股卡片 {c['ticker']} 指標應為 2~4 個")
                    continue
                c["metrics"] = m
            c["news"] = news
            if u.get("tags"):
                c["tags"] = u["tags"][:3]
            c["updated_on"] = day
            done.append(c["ticker"])
        if done:
            d["updated_at"] = day
            US_STOCKS.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"📈 美股卡片更新 {len(done)} 家:{done}")

    # 4. 與週報 PR 相同的格式、連結檢查 (事實查核由本機 Claude 逐條完成)
    from verify_weekly import changed_cards, check_format, check_links
    archive = json.loads((DATA_DIR / "news_archive.json").read_text(encoding="utf-8"))["items"]
    allowed = {normalize_url(i["link"]) for i in items} | {normalize_url(a["url"]) for a in archive}
    cards = [("美股", c) for c in changed_cards("data/us_stocks.json")]
    errors += check_format(tag, post, graph, cards) + check_links(post, graph, allowed)
    for e in errors:
        print(f"  ✗ {e}")
    print("PASSED" if not errors else f"FAILED ({len(errors)} 項)")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("prepare", "finalize"):
        sys.exit(__doc__)
    {"prepare": prepare, "finalize": finalize}[sys.argv[1]](Path(sys.argv[2]))
