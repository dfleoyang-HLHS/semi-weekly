#!/usr/bin/env python3
"""
generate_news_brief.py
讀取 fetch_news.py 抓到的 raw_news.json,
產生「新聞快訊」(news brief) — 不需要 Claude 撰寫,直接整理成清單。

輸出: posts/news/YYYY-MM-DD-brief.md
"""

import json
from datetime import date
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
POSTS_DIR = ROOT / "posts"
NEWS_DIR = POSTS_DIR / "news"
NEWS_DIR.mkdir(parents=True, exist_ok=True)


# 關鍵字 → 公司對照表 (用於自動標記公司)
COMPANY_KEYWORDS = {
    "TSMC": ["TSMC", "台積電", "台積", "tsmc"],
    "ASE": ["ASE", "日月光"],
    "KYEC": ["京元電", "KYEC"],
    "PTI": ["力成", "PTI"],
    "Amkor": ["Amkor", "艾克爾"],
    "NVIDIA": ["NVIDIA", "輝達", "Nvidia"],
    "AMD": [" AMD ", "超微"],
    "Intel": ["Intel", "英特爾"],
    "Broadcom": ["Broadcom", "博通"],
    "SK Hynix": ["SK Hynix", "海力士", "SK海力士"],
    "Samsung": ["Samsung", "三星"],
    "Micron": ["Micron", "美光"],
    "Ibiden": ["Ibiden"],
    "Shinko": ["Shinko"],
    "Ajinomoto": ["Ajinomoto", "味之素"],
    "JCET": ["JCET", "長電", "长电"],
    "TFME": ["TFME", "通富微電", "通富微电"],
    "SMIC": ["SMIC", "中芯"],
    "BESI": ["BESI", "Besi"],
    "ASML": ["ASML"],
    "AT&S": ["AT&S", "AT＆S"],
}

# 關鍵字 → 區域
REGION_KEYWORDS = {
    "台灣": ["台積", "日月光", "京元", "力成", "欣興", "南電", "景碩", "台灣", "Taiwan", "TSMC"],
    "美國": ["NVIDIA", "輝達", "AMD", "Intel", "Amkor", "Broadcom", "Apple", "Micron",
            "美國", "USA", "Arizona", "亞利桑那"],
    "韓國": ["SK Hynix", "Samsung", "海力士", "三星", "韓國", "Korea"],
    "日本": ["Ibiden", "Shinko", "Resonac", "Ajinomoto", "日本", "Japan", "Sony"],
    "中國大陸": ["JCET", "長電", "通富", "中芯", "SMIC", "華為", "Huawei",
              "大陸", "中國", "China"],
    "歐洲": ["ASML", "BESI", "AT&S", "Infineon", "STMicro", "歐洲", "Europe"],
}


def detect_companies(text):
    """從文字偵測涉及的公司"""
    found = []
    for company, keywords in COMPANY_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text.lower():
                found.append(company)
                break
    return found


def detect_regions(text):
    """從文字偵測涉及的區域"""
    found = []
    for region, keywords in REGION_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text.lower():
                found.append(region)
                break
    return found


def main():
    raw_path = DATA_DIR / "raw_news.json"
    if not raw_path.exists():
        raise RuntimeError(f"找不到 {raw_path}")

    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    items = raw["items"]
    today = date.today()

    if not items:
        print("⚠️  本日無相關新聞,跳過快訊生成")
        return

    # 統計
    all_companies = []
    all_regions = []
    by_source = defaultdict(list)

    for item in items:
        text = item.get("title", "") + " " + item.get("summary", "")
        item["_companies"] = detect_companies(text)
        item["_regions"] = detect_regions(text)
        all_companies.extend(item["_companies"])
        all_regions.extend(item["_regions"])
        by_source[item["source"]].append(item)

    # 取最常出現的公司與區域作為 metadata
    from collections import Counter
    top_companies = [c for c, _ in Counter(all_companies).most_common(10)]
    top_regions = list(set(all_regions))

    # 產生 Markdown
    weekday_names = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"]
    weekday = weekday_names[today.weekday()]

    md_lines = [
        "---",
        f'title: "新聞快訊 ({today.isoformat()} {weekday})"',
        f"date: {today.isoformat()}",
        f'week: "{today.isocalendar()[0]}-W{today.isocalendar()[1]:02d}"',
        f'category: "新聞快訊"',
        f"regions: {json.dumps(top_regions, ensure_ascii=False)}",
        f"companies: {json.dumps(top_companies, ensure_ascii=False)}",
        f'tags: ["新聞快訊", "半導體", "AI 供應鏈"]',
        f'summary: "本日抓取 {len(items)} 則半導體與 AI 供應鏈相關新聞,涵蓋 {len(top_regions)} 個區域、{len(top_companies)} 家主要公司。"',
        "---",
        "",
        f"# 📰 半導體新聞快訊 ({today.isoformat()} {weekday})",
        "",
        f"**抓取 {len(items)} 則相關新聞**,自動分類整理。深度分析請見每週一發布的週報。",
        "",
        "---",
        "",
    ]

    # 依公司分類顯示
    if top_companies:
        md_lines.append("## 🏢 本日重點公司")
        md_lines.append("")
        md_lines.append(" · ".join(f"**{c}**" for c in top_companies[:8]))
        md_lines.append("")

    # 依來源分組顯示新聞
    md_lines.append("## 📋 新聞列表(依來源)")
    md_lines.append("")

    for source, news_list in by_source.items():
        md_lines.append(f"### {source} ({len(news_list)} 則)")
        md_lines.append("")
        for n in news_list:
            title = n.get("title", "").strip()
            link = n.get("link", "")
            published = n.get("published", "")[:10] if n.get("published") else ""
            companies = n.get("_companies", [])

            line = f"- [{title}]({link})"
            if published:
                line += f" — `{published}`"
            md_lines.append(line)

            if companies:
                md_lines.append(f"  - 🏢 {' · '.join(companies)}")

            summary = n.get("summary", "")
            if summary:
                # 移除 HTML 標籤、限長
                import re
                clean = re.sub(r"<[^>]+>", "", summary).strip()
                if len(clean) > 150:
                    clean = clean[:150] + "..."
                if clean:
                    md_lines.append(f"  - {clean}")
        md_lines.append("")

    md_lines.append("---")
    md_lines.append("")
    md_lines.append("*本快訊由系統自動產生,無人工撰寫。深度產業分析請見每週一的週報。*")

    # 寫檔
    filename = f"{today.isoformat()}-brief.md"
    out_path = NEWS_DIR / filename
    out_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"✅ 快訊生成完成")
    print(f"   📄 {out_path}")
    print(f"   📰 新聞數: {len(items)}")
    print(f"   🏢 公司數: {len(top_companies)}")
    print(f"   📍 區域數: {len(top_regions)}")


if __name__ == "__main__":
    main()
