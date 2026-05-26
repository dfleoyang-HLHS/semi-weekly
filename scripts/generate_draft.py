#!/usr/bin/env python3
"""
generate_draft.py
讀取 data/raw_news.json,呼叫 Claude API 生成本週週報草稿。
輸出: posts/draft-YYYY-WNN-semi-weekly.md (草稿,不會被 build_index 索引)

依賴: pip install anthropic
環境變數: ANTHROPIC_API_KEY
"""

import os
import json
from datetime import date
from pathlib import Path

import anthropic

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
POSTS_DIR = ROOT / "posts"
TEMPLATE = ROOT / "scripts" / "weekly_template.md"


SYSTEM_PROMPT = """你是專業的半導體產業分析師,負責每週撰寫一份「半導體 + AI 供應鏈週報」。

撰寫原則:
1. 用繁體中文撰寫,專業且簡潔
2. 嚴格依照模板的章節結構 (美國、台灣、日本、韓國、中國大陸、歐洲)
3. 每家公司的描述要包含:近期動態 / 財報數字 (如有) / 對 CoWoS 或 AI 供應鏈的影響
4. 引用具體數字 (營收、產能、市占率) 比抽象描述更有價值
5. 「本週重點」用 3-5 句話總結最重要的事
6. 「風險與下週觀察點」要具體可追蹤,不要寫成空泛的趨勢
7. 若某區域本週無重大事件,直接寫「本週無重大進展」,不要硬湊

輸出格式:
- 完整的 Markdown,包含 YAML front matter
- companies 欄位列出本週實際提及的公司
- tags 欄位列出本週的核心議題
"""


def build_user_prompt(news_items, year, week, today_iso):
    items_text = "\n\n".join([
        f"[{i+1}] {item['title']}\n來源: {item['source']} | 發布: {item['published']}\n摘要: {item['summary']}\n連結: {item['link']}"
        for i, item in enumerate(news_items[:80])  # 限制 80 則避免 token 爆掉
    ])

    return f"""請依照以下模板,根據本週新聞撰寫週報。

【目前資訊】
- 年份: {year}
- 週次: W{week:02d}
- 日期: {today_iso}

【本週模板】
{TEMPLATE.read_text(encoding='utf-8')}

【本週相關新聞 (過去 7 天)】
{items_text}

請輸出完整的 Markdown 週報 (含 front matter),不要包含任何說明文字。"""


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("請設定環境變數 ANTHROPIC_API_KEY")

    raw_path = DATA_DIR / "raw_news.json"
    if not raw_path.exists():
        raise RuntimeError(f"找不到 {raw_path},請先執行 fetch_news.py")

    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    items = raw["items"]
    if not items:
        print("⚠️  本週無相關新聞,跳過生成")
        return

    today = date.today()
    iso = today.isocalendar()
    year, week = iso[0], iso[1]

    print(f"呼叫 Claude API 生成 {year}-W{week:02d} 週報...")
    print(f"輸入新聞: {len(items)} 則")

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=8000,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": build_user_prompt(items, year, week, today.isoformat())
        }],
    )

    draft_text = response.content[0].text

    out_path = POSTS_DIR / f"draft-{year}-W{week:02d}-semi-weekly.md"
    out_path.write_text(draft_text, encoding="utf-8")

    print(f"\n✅ 草稿生成完成: {out_path}")
    print(f"   下一步: 人工審閱 → 移除 draft- 前綴 → git commit")


if __name__ == "__main__":
    main()
