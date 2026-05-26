#!/usr/bin/env python3
"""prepare_prompt.py - 把新聞整理成可貼到 Claude Pro 的提示包"""

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE = ROOT / "scripts" / "weekly_template.md"

SYSTEM_INSTRUCTION = """你是專業的半導體產業分析師,請依照下方提供的「週報模板」與「本週新聞清單」撰寫本週的半導體 + AI 供應鏈週報。

撰寫原則:
1. 用繁體中文撰寫,專業且簡潔
2. 嚴格依照模板的章節結構 (美國、台灣、日本、韓國、中國大陸、歐洲)
3. 每家公司的描述要包含:近期動態 / 財報數字 / 對 AI 供應鏈的影響
4. 引用具體數字 (營收、產能、市占率) 比抽象描述有價值
5. 「本週重點」用 3-5 句話總結最重要的事
6. 「風險與下週觀察點」要具體可追蹤
7. 若某區域本週無重大事件,直接寫「本週無重大進展」
8. 完成的週報請包含 YAML front matter (date, week, companies, tags, summary)

輸出格式:完整的 Markdown,可直接存成 .md 檔案。
"""


def main():
    raw_path = DATA_DIR / "raw_news.json"
    if not raw_path.exists():
        raise RuntimeError(f"找不到 {raw_path},請先執行 fetch_news.py")

    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    items = raw["items"]
    today = date.today()
    iso = today.isocalendar()
    year, week = iso[0], iso[1]

    by_source = {}
    for item in items:
        by_source.setdefault(item["source"], []).append(item)

    summary_lines = [
        f"# 本週新聞摘要 ({year}-W{week:02d})",
        f"",
        f"**抓取時間**: {raw['fetched_at']}",
        f"**總篇數**: {len(items)} 則",
        f"",
        f"---",
        f"",
    ]
    for source, news_list in by_source.items():
        summary_lines.append(f"## {source} ({len(news_list)} 則)\n")
        for n in news_list:
            summary_lines.append(f"- [{n['title']}]({n['link']})")
            if n.get("published"):
                summary_lines.append(f"  - 📅 {n['published'][:10]}")
        summary_lines.append("")

    (DATA_DIR / "weekly_summary.md").write_text(
        "\n".join(summary_lines), encoding="utf-8"
    )

    template_content = TEMPLATE.read_text(encoding="utf-8")

    news_block_lines = []
    for i, item in enumerate(items[:80], 1):
        news_block_lines.append(f"### [{i}] {item['title']}")
        news_block_lines.append(f"- 來源: {item['source']}")
        if item.get("published"):
            news_block_lines.append(f"- 日期: {item['published'][:10]}")
        news_block_lines.append(f"- 連結: {item['link']}")
        if item.get("summary"):
            news_block_lines.append(f"- 摘要: {item['summary']}")
        news_block_lines.append("")

    prompt_content = f"""# 本週週報生成提示 ({year}-W{week:02d})

> 📋 **使用方式**:
> 1. 全選此檔案內容 (Ctrl+A) 並複製 (Ctrl+C)
> 2. 打開 https://claude.ai
> 3. 開新對話,貼上 (Ctrl+V) → 送出
> 4. Claude 回覆完整週報後,複製內容
> 5. 在 `posts/` 建立新檔案 `{year}-W{week:02d}-semi-weekly.md`
> 6. 貼上週報內容並 commit

---

## 指示

{SYSTEM_INSTRUCTION}

---

## 目前資訊

- 年份: {year}
- 週次: W{week:02d}
- 日期: {today.isoformat()}

---

## 週報模板

{template_content}

---

## 本週相關新聞 ({len(items)} 則)

{chr(10).join(news_block_lines)}

---

請依照模板輸出完整的 Markdown 週報 (含 YAML front matter)。
"""

    (DATA_DIR / "weekly_prompt.md").write_text(prompt_content, encoding="utf-8")

    print(f"✅ 提示包生成完成")
    print(f"   📄 data/weekly_prompt.md")
    print(f"   📋 data/weekly_summary.md")
    print(f"   📰 新聞總數: {len(items)} 則")


if __name__ == "__main__":
    main()
