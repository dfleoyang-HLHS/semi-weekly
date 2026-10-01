#!/usr/bin/env python3
"""
generate_draft.py
讀取 data/raw_news.json,呼叫 Claude API 產生本週:
  1. 週報        posts/YYYY-WNN-semi-weekly.md
  2. 供應鏈圖資料 data/supplychain-YYYY-WNN.json (以上一期圖為基礎增修)

檔案直接以正式檔名輸出;由 GitHub Actions 開成 Pull Request,
人工審閱後按 Merge 即發佈 (merge 後 build_index.py 會更新 supplychain-index.json)。

依賴: pip install anthropic
環境變數: ANTHROPIC_API_KEY
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import anthropic

from archive_news import normalize_url, url_to_id

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
POSTS_DIR = ROOT / "posts"
TEMPLATE = ROOT / "scripts" / "weekly_template.md"

MODEL = "claude-opus-5-5"
TZ = timezone(timedelta(hours=8))  # 台灣時間 (無日光節約)
FALLBACK_BETA = "server-side-fallback-2026-07-01"


WEEKLY_SYSTEM = """你是專業的半導體產業分析師,負責每週撰寫一份「半導體 + AI 供應鏈週報」。

撰寫原則:
1. 用繁體中文撰寫,專業且簡潔
2. 嚴格依照模板的章節結構 (美國、台灣、日本、韓國、中國大陸、歐洲)
3. 每家公司的描述要包含:近期動態 / 財報數字 (如有) / 對 CoWoS 或 AI 供應鏈的影響
4. 只使用新聞清單中出現的數字與事實;新聞沒有提供的數字不要自行補上,寧可寫「待確認」
5. 「本週重點」用 3-5 句話總結最重要的事
6. 「風險與下週觀察點」要具體可追蹤,不要寫成空泛的趨勢
7. 若某區域本週無重大事件,直接寫「本週無重大進展」,不要硬湊
8. 重要論點在句尾以 [n] 標註對應的新聞編號,文末附「參考來源」列出編號、標題與連結

輸出格式:
- 完整的 Markdown,以 YAML front matter 開頭 (title, date, week, category, regions, companies, tags, summary)
- companies 欄位列出本週實際提及的公司;tags 欄位列出本週的核心議題
- 只輸出週報本身,不要有任何前言或說明文字,也不要用 ``` 包住
"""

SUPPLYCHAIN_SYSTEM = """你負責維護網站上的「半導體 + AI 供應鏈關係圖」資料。
你會拿到上一期的圖 (JSON) 與本週剛完成的週報,請產出本週版本的圖:

1. 以上一期為基礎增修,不要整張重畫;保留仍然有效的節點與關係,id 維持不變
2. 依本週週報更新節點的 sub (一句話,15 字以內,反映本週最新動態,例如產能、財報、事件)
3. 本週週報出現的重要新公司或新關係才新增;明顯過時的才刪除
4. tier: up = 上游 (材料、設備、載板), mid = 中游 (晶圓代工、封測、記憶體), down = 下游 (IC 設計、雲端、系統廠)
5. region 只能是 US / TW / JP / KR / CN / EU
6. edge.type: supply (供應) / cooperation (合作) / alliance (結盟、入股) / competition (競爭) / hostility (制裁、訴訟、對立)
7. 每條 edge 的 from / to 必須是 nodes 中存在的 id
8. highlights 為 6-10 條本週重點 (每條一句,含具體數字);summary 為 2-3 句總結;title 為本週主題 (以「 · 」分隔兩個重點)
9. 全部使用繁體中文 (公司英文名稱可保留)
10. 每個節點的 news_ref 填入與該公司最相關、最關鍵的一則新聞編號 (新聞清單中的 [n]);
    本週沒有該公司的相關新聞就填 0,不要勉強對應
"""

SUPPLYCHAIN_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "highlights": {"type": "array", "items": {"type": "string"}},
        "nodes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "tier": {"type": "string", "enum": ["up", "mid", "down"]},
                    "label": {"type": "string"},
                    "sub": {"type": "string"},
                    "region": {"type": "string", "enum": ["US", "TW", "JP", "KR", "CN", "EU"]},
                    "news_ref": {"type": "integer"},
                },
                "required": ["id", "tier", "label", "sub", "region", "news_ref"],
                "additionalProperties": False,
            },
        },
        "edges": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "from": {"type": "string"},
                    "to": {"type": "string"},
                    "type": {
                        "type": "string",
                        "enum": ["supply", "cooperation", "alliance", "competition", "hostility"],
                    },
                    "label": {"type": "string"},
                },
                "required": ["from", "to", "type", "label"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["title", "summary", "highlights", "nodes", "edges"],
    "additionalProperties": False,
}


def call_claude(client, system, user, **extra):
    """串流呼叫 Claude,回傳最終 text;遇到 refusal / max_tokens 直接中止。"""
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=64000,
        betas=[FALLBACK_BETA],
        fallbacks="default",
        thinking={"type": "adaptive"},
        system=system,
        messages=[{"role": "user", "content": user}],
        **extra,
    ) as stream:
        msg = stream.get_final_message()

    if msg.stop_reason == "refusal":
        raise RuntimeError(f"Claude 拒絕回應: {msg.stop_details}")
    if msg.stop_reason == "max_tokens":
        raise RuntimeError("輸出超過 max_tokens 被截斷")
    print(f"   tokens: in={msg.usage.input_tokens} out={msg.usage.output_tokens}")
    return "".join(b.text for b in msg.content if b.type == "text").strip()


def build_news_block(items):
    return "\n\n".join(
        f"[{i}] {it['title']}\n來源: {it['source']} | 發布: {it['published'][:10]}\n"
        f"摘要: {re.sub(r'<[^>]+>', '', it.get('summary', '')).strip()}\n連結: {it['link']}"
        for i, it in enumerate(items[:80], 1)  # 限制 80 則
    )


def latest_supplychain(exclude_week):
    """找出最新一期 (排除本週) 的供應鏈 JSON 作為基礎。"""
    files = sorted(
        p for p in DATA_DIR.glob("supplychain-*-W*.json")
        if not p.name.endswith(f"{exclude_week}.json")
    )
    return json.loads(files[-1].read_text(encoding="utf-8")) if files else None


def strip_fence(text):
    m = re.match(r"^```(?:markdown|md)?\s*\n(.*)\n```\s*$", text, re.DOTALL)
    return m.group(1) if m else text


def attach_news(graph, items, prev):
    """把 news_ref 編號換成實際新聞標題與連結;本週無新聞的節點沿用上一期的連結。"""
    prev_news = {n["id"]: n["news"] for n in (prev or {}).get("nodes", []) if n.get("news")}
    archive_ids = url_to_id()  # 對照新聞資料庫的永久編號
    linked = 0
    for n in graph["nodes"]:
        ref = n.pop("news_ref", 0)
        if 1 <= ref <= min(len(items), 80):
            it = items[ref - 1]
            n["news"] = {"title": it["title"], "url": it["link"], "date": it["published"][:10]}
            if aid := archive_ids.get(normalize_url(it["link"])):
                n["news"] = {"id": aid, **n["news"]}
            linked += 1
        elif n["id"] in prev_news:
            n["news"] = prev_news[n["id"]]
    carried = sum(1 for n in graph["nodes"] if n.get("news")) - linked
    print(f"   新聞連結: 本週 {linked} 家,沿用上期 {carried} 家")
    return graph


def validate_graph(graph):
    ids = {n["id"] for n in graph["nodes"]}
    if len(ids) != len(graph["nodes"]):
        raise RuntimeError("供應鏈圖有重複的節點 id")
    before = len(graph["edges"])
    graph["edges"] = [e for e in graph["edges"] if e["from"] in ids and e["to"] in ids]
    if len(graph["edges"]) != before:
        print(f"   ⚠️  移除 {before - len(graph['edges'])} 條指向不存在節點的關係")
    return graph


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("請設定環境變數 ANTHROPIC_API_KEY (GitHub: Settings → Secrets → Actions)")

    raw_path = DATA_DIR / "raw_news.json"
    if not raw_path.exists():
        sys.exit(f"找不到 {raw_path},請先執行 fetch_news.py")
    items = json.loads(raw_path.read_text(encoding="utf-8"))["items"]
    if not items:
        print("⚠️  本週無相關新聞,跳過生成")
        return

    today = datetime.now(TZ).date()
    year, week, _ = today.isocalendar()
    week_tag = f"{year}-W{week:02d}"
    client = anthropic.Anthropic()

    # 1. 週報
    print(f"📝 產生 {week_tag} 週報 (新聞 {len(items)} 則)...")
    weekly_md = strip_fence(call_claude(
        client,
        WEEKLY_SYSTEM,
        f"【目前資訊】\n- 週次: {week_tag}\n- 日期: {today.isoformat()}\n\n"
        f"【週報模板】\n{TEMPLATE.read_text(encoding='utf-8')}\n\n"
        f"【本週相關新聞 (過去 7 天)】\n{build_news_block(items)}\n\n"
        "請依模板輸出完整的 Markdown 週報。",
    ))
    if not weekly_md.startswith("---"):
        raise RuntimeError("週報缺少 YAML front matter,請檢查輸出")
    post_path = POSTS_DIR / f"{week_tag}-semi-weekly.md"
    post_path.write_text(weekly_md + "\n", encoding="utf-8")
    print(f"   ✅ {post_path.relative_to(ROOT)}")

    # 2. 供應鏈圖
    prev = latest_supplychain(week_tag)
    print(f"🔗 更新供應鏈圖 (基礎: {prev['week'] if prev else '無'})...")
    graph_text = call_claude(
        client,
        SUPPLYCHAIN_SYSTEM,
        f"【上一期供應鏈圖】\n{json.dumps(prev, ensure_ascii=False) if prev else '(無,請從頭建立)'}\n\n"
        f"【本週週報 ({week_tag})】\n{weekly_md}\n\n"
        f"【本週新聞清單 (news_ref 請填這裡的編號)】\n{build_news_block(items)}",
        output_config={"format": {"type": "json_schema", "schema": SUPPLYCHAIN_SCHEMA}},
    )
    graph = attach_news(validate_graph(json.loads(graph_text)), items, prev)
    graph = {"week": week_tag, "date": today.isoformat(), **graph}
    sc_path = DATA_DIR / f"supplychain-{week_tag}.json"
    sc_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"   ✅ {sc_path.relative_to(ROOT)} ({len(graph['nodes'])} 節點 / {len(graph['edges'])} 關係)")

    # 給 GitHub Actions 開 PR 用
    if gh_out := os.environ.get("GITHUB_OUTPUT"):
        with open(gh_out, "a", encoding="utf-8") as f:
            f.write(f"week_tag={week_tag}\n")
            f.write(f"title={graph['title']}\n")


if __name__ == "__main__":
    main()
