#!/usr/bin/env python3
"""
verify_weekly.py
週報 PR 的自動查核 (在 generate_draft.py 之後執行)。全部通過才會標記 auto-merge-ok,
週一 20:00 (台灣時間) 自動 Merge;任何一項未通過則標記 needs-review,等人工處理。

查核項目:
  1. 格式:週報 front matter、供應鏈圖結構 (節點 / 關係 / 分析)、美股與台股卡片格式
  2. 連結:週報與供應鏈圖中的新聞連結,都必須來自已抓取的新聞 (不得是 AI 自行產生的網址)
  3. 事實查核:由 Claude 獨立比對週報、供應鏈分析與本週更新的卡片中的數字與事件,是否有新聞依據

用法: python scripts/verify_weekly.py 2026-W41 "PR 標題"
輸出:
  - pr_body.md (PR 內文,含查核報告;不會 commit)
  - GITHUB_OUTPUT: passed=true|false
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from archive_news import normalize_url, week_news  # noqa: E402

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
BODY = ROOT / "pr_body.md"

FACT_SYSTEM = """你是嚴格的財經事實查核員。你會拿到「本週新聞清單」(唯一的事實依據) 與待查核的內容。
請逐一檢查待查核內容中的具體數字、金額、百分比、日期、排名與事件:
- 必須能在新聞清單的標題或摘要中找到依據;合理的換算、四捨五入、中英文或幣別單位轉換可以接受
- 沒有依據、與新聞矛盾、或把「傳聞」寫成「確定」的,列入 issues
- 「目前卡片」中標示為沿用的舊內容不需查核;只查核本次新增或改寫的內容
- 不要評論文筆、結構或觀點,只看事實
沒有問題時 issues 回傳空陣列。"""

FACT_SCHEMA = {
    "type": "object",
    "properties": {
        "checked_claims": {"type": "integer"},
        "issues": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "where": {"type": "string"},
                    "claim": {"type": "string"},
                    "problem": {"type": "string"},
                },
                "required": ["where", "claim", "problem"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["checked_claims", "issues"],
    "additionalProperties": False,
}


def git_show(path):
    """取得 commit 前 (main 上) 的檔案內容;不存在時回傳 None"""
    r = subprocess.run(["git", "show", f"HEAD:{path}"], cwd=ROOT, capture_output=True)
    return r.stdout.decode("utf-8") if r.returncode == 0 else None


def changed_cards(rel_path):
    """回傳本次有變動的個股卡片"""
    p = ROOT / rel_path
    if not p.exists():
        return []
    new = json.loads(p.read_text(encoding="utf-8"))["stocks"]
    old_text = git_show(rel_path)
    old = {c["ticker"]: c for c in json.loads(old_text)["stocks"]} if old_text else {}
    return [c for c in new if old.get(c["ticker"]) != c]


def check_format(week, post, graph, cards):
    errors = []
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", post, re.DOTALL)
    meta = yaml.safe_load(m.group(1)) if m else None
    if not isinstance(meta, dict):
        errors.append("週報缺少或無法解析 YAML front matter")
    else:
        for k in ["title", "date", "week", "companies", "tags", "summary"]:
            if not meta.get(k):
                errors.append(f"週報 front matter 缺少 `{k}`")
        if meta.get("week") and str(meta["week"]) != week:
            errors.append(f"週報週次 `{meta['week']}` 與 `{week}` 不符")
    for sec in ["## 本週重點", "## 資料來源"]:
        if sec not in post and not (sec == "## 資料來源" and "## 參考來源" in post):
            errors.append(f"週報缺少「{sec[3:]}」章節")
    if len(post) < 3000:
        errors.append(f"週報內容過短 ({len(post)} 字元)")

    ids = {n["id"] for n in graph.get("nodes", [])}
    tiers = {n["tier"] for n in graph.get("nodes", [])}
    if len(graph.get("nodes", [])) < 15:
        errors.append(f"供應鏈圖節點過少 ({len(graph.get('nodes', []))})")
    if not {"up", "mid", "down"} <= tiers:
        errors.append("供應鏈圖缺少上 / 中 / 下游其中一層")
    bad = [e for e in graph.get("edges", []) if e["from"] not in ids or e["to"] not in ids]
    if bad:
        errors.append(f"供應鏈圖有 {len(bad)} 條關係指向不存在的公司")
    an = graph.get("analysis") or {}
    for k in ["overview", "supply", "cooperation", "alliance", "competition", "hostility"]:
        if not an.get(k):
            errors.append(f"供應鏈分析缺少 `{k}`")

    for page, c in cards:
        if not (isinstance(c.get("metrics"), dict) and len(c["metrics"]) >= 1):
            errors.append(f"{page} {c['ticker']} 指標格式錯誤")
        if not (isinstance(c.get("news"), list) and len(c["news"]) >= 2):
            errors.append(f"{page} {c['ticker']} 近期重點少於 2 條")
    return errors


def check_links(post, graph, allowed):
    errors = []
    for url in re.findall(r"\]\((https?://[^)\s]+)\)", post):
        if normalize_url(url) not in allowed:
            errors.append(f"週報連結不在已抓取的新聞中:{url}")
    for n in graph.get("nodes", []):
        url = (n.get("news") or {}).get("url")
        if url and normalize_url(url) not in allowed:
            errors.append(f"供應鏈圖 {n['id']} 的新聞連結不在新聞資料庫中:{url}")
    return errors


def fact_check(post, graph, cards, items):
    from generate_draft import build_news_block, call_claude  # 延後匯入:只有需要時才載入 anthropic
    import anthropic

    content = {
        "週報": post,
        "供應鏈圖 (標題、重點、各公司近況、關係分析)": {
            "title": graph.get("title"), "summary": graph.get("summary"),
            "highlights": graph.get("highlights"), "analysis": graph.get("analysis"),
            "nodes": [{"label": n["label"], "sub": n["sub"]} for n in graph.get("nodes", [])],
        },
        "本次更新的個股卡片": [{"page": p, "ticker": c["ticker"], "name": c["name"],
                         "metrics": c["metrics"], "news": c["news"]} for p, c in cards],
    }
    result = json.loads(call_claude(
        anthropic.Anthropic(),
        FACT_SYSTEM,
        f"【本週新聞清單】\n{build_news_block(items)}\n\n"
        f"【待查核內容】\n{json.dumps(content, ensure_ascii=False, indent=1)}",
        output_config={"format": {"type": "json_schema", "schema": FACT_SCHEMA}},
    ))
    return result


def main():
    week, title = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "")
    post = (ROOT / "posts" / f"{week}-semi-weekly.md").read_text(encoding="utf-8")
    graph = json.loads((DATA / f"supplychain-{week}.json").read_text(encoding="utf-8"))
    items = week_news(7)  # 與 generate_draft.py 使用同一份新聞清單
    archive = json.loads((DATA / "news_archive.json").read_text(encoding="utf-8"))["items"]
    allowed = {normalize_url(i["link"]) for i in items} | {normalize_url(a["url"]) for a in archive}
    cards = [("美股", c) for c in changed_cards("data/us_stocks.json")] + \
            [("台股", c) for c in changed_cards("data/tw_stocks.json")]

    sections, passed = [], True

    fmt = check_format(week, post, graph, cards)
    sections.append(("格式", fmt))
    links = check_links(post, graph, allowed)
    sections.append(("連結", links))
    passed = not fmt and not links

    try:
        fc = fact_check(post, graph, cards, items)
        issues = [f"**{i['where']}**:「{i['claim']}」— {i['problem']}" for i in fc["issues"]]
        sections.append((f"事實查核 (檢查 {fc['checked_claims']} 項)", issues))
        passed = passed and not issues
    except Exception as e:  # 查核本身失敗時不放行
        sections.append(("事實查核", [f"查核程式執行失敗:{e}"]))
        passed = False

    lines = [f"Claude 已自動產生 **{week}** 週報、供應鏈圖{'與個股卡片' if cards else ''}。", ""]
    if passed:
        lines += ["### ✅ 自動查核通過",
                  "此 PR 已標記 `auto-merge-ok`,將於 **週一 20:00 (台灣時間)** 自動 Merge 並發佈。",
                  "- 想先修改:直接在 Files changed 編輯 (… → Edit file),20:00 會連同修改一起發佈",
                  "- 不要自動發佈:加上 `hold` 標籤,或直接 Close 此 PR", ""]
    else:
        lines += ["### ⚠️ 自動查核未通過",
                  "此 PR 已標記 `needs-review`,**不會自動 Merge**。請修正下列問題後手動 Merge,或 Close。", ""]
    for name, errs in sections:
        lines.append(f"#### {'✅' if not errs else '❌'} {name}")
        lines += [f"- {e}" for e in errs] or ["- 無問題"]
        lines.append("")
    lines += ["#### 本次變更",
              f"- 週報:`posts/{week}-semi-weekly.md`",
              f"- 供應鏈圖:`data/supplychain-{week}.json`"]
    if cards:
        changed = ", ".join(f"{p} {c['ticker']}" for p, c in cards)
        lines.append(f"- 個股卡片:{changed}")
    BODY.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n".join(lines))
    if gh_out := os.environ.get("GITHUB_OUTPUT"):
        with open(gh_out, "a", encoding="utf-8") as f:
            f.write(f"passed={'true' if passed else 'false'}\n")


if __name__ == "__main__":
    main()
