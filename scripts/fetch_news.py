#!/usr/bin/env python3
"""
fetch_news.py
抓取過去 7 天的半導體 + AI 供應鏈新聞,輸出到 data/raw_news.json
供 generate_draft.py 使用。

來源:
  - DigiTimes 中英文 RSS
  - TrendForce (feed_v2,加參數避開 CDN 快取)
  - 鉅亨網 台股 / 美股
  - TechNews 科技新報
  - SemiWiki
每個來源若無文章或最新文章超出抓取期間,會印出 ⚠️ 警示。

依賴: pip install feedparser requests
"""

import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# RSS 來源清單 — 可自行擴充
FEEDS = [
    # 台灣中文媒體
    ("TechNews 科技新報", "https://technews.tw/feed/"),
    # 鉅亨網舊網址 /rss/cat/tech 已失效 (404),新版科技分類 RSS 為空,改用台股與美股分類
    ("鉅亨網 台股", "https://news.cnyes.com/rss/v1/news/category/tw_stock"),
    ("鉅亨網 美股", "https://news.cnyes.com/rss/v1/news/category/wd_stock"),
    ("DigiTimes 中文", "https://www.digitimes.com.tw/rss/news.xml"),
    # 國際
    ("DigiTimes Asia", "https://www.digitimes.com/rss/daily.xml"),
    # TrendForce 的 CDN 會長期快取舊版 feed (曾停在 2026-07-01),需加參數取得最新內容
    ("TrendForce", "https://www.trendforce.com/news/feed_v2/", {"bust_cache": True}),
    ("SemiWiki", "https://semiwiki.com/feed/"),
    # 關鍵字篩選用
]

# 半導體 + AI 供應鏈關鍵字 (中英文)
KEYWORDS = [
    # 技術
    "CoWoS", "CoPoS", "CoWoP", "SoIC", "HBM", "HBM4", "HBM4E",
    "advanced packaging", "先進封裝", "面板級封裝", "FOPLP",
    "hybrid bonding", "混合鍵合", "interposer", "中介層",
    "ABF", "chiplet", "晶圓代工", "後段封測",
    # 公司
    "TSMC", "台積電", "ASE", "日月光", "Amkor", "KYEC", "京元電",
    "SPIL", "矽品", "PTI", "力成", "Unimicron", "欣興",
    "NVIDIA", "輝達", "AMD", "Intel", "Broadcom",
    "SK Hynix", "海力士", "Samsung", "三星", "Micron", "美光",
    "Ibiden", "Shinko", "Resonac", "Ajinomoto",
    "JCET", "長電科技", "TFME", "通富微電", "SMIC", "中芯",
    "BESI", "ASML", "Applied Materials",
    "Marvell", "邁威爾", "Meta", "Tesla", "特斯拉", "Acer", "宏碁", "Winbond", "華邦",
    "UMC", "聯電", "華星光", "尖點",
    # 應用
    "AI chip", "AI 晶片", "GPU", "TPU", "ASIC",
    "data center", "資料中心", "Rubin", "Blackwell",
]


def is_relevant(entry):
    """檢查標題或摘要是否包含關鍵字 (英文以完整單字比對,避免 base→ASE、metal→Meta 誤判)"""
    from generate_news_brief import keyword_in
    text = entry.get("title", "") + " " + entry.get("summary", "")
    return any(keyword_in(kw, text) for kw in KEYWORDS)


def parse_date(entry):
    """從 RSS entry 解析發布日期"""
    for key in ("published_parsed", "updated_parsed"):
        t = entry.get(key)
        if t:
            return datetime.fromtimestamp(time.mktime(t), tz=timezone.utc)
    return None


def fetch_all(days_back=7):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
    all_items = []
    seen_links = set()  # 同一則新聞可能出現在多個分類,依連結去重

    for source_name, url, *opts in FEEDS:
        opts = opts[0] if opts else {}
        if opts.get("bust_cache"):
            url += ("&" if "?" in url else "?") + f"nc={int(time.time())}"
        print(f"抓取: {source_name}")
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print(f"  ❌ 失敗: {e}")
            continue

        dates = [d for d in (parse_date(e) for e in feed.entries) if d]
        newest = max(dates) if dates else None
        kept = 0
        for entry in feed.entries:
            pub_date = parse_date(entry)
            if pub_date and pub_date < cutoff:
                continue
            if not is_relevant(entry):
                continue
            link = entry.get("link", "")
            if link in seen_links:
                continue
            seen_links.add(link)
            kept += 1

            all_items.append({
                "source": source_name,
                "title": entry.get("title", "").strip(),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", "")[:500],
                "published": pub_date.isoformat() if pub_date else "",
            })

        print(f"  ✅ 取得 {len(feed.entries)} 篇,{days_back} 天內符合關鍵字 {kept} 篇"
              + (f" (最新 {newest:%Y-%m-%d})" if newest else ""))
        # 來源異常警示:沒有任何文章,或最新一篇已超出抓取期間 (可能停更或被快取)
        if not feed.entries:
            print(f"  ⚠️  {source_name} 沒有回傳任何文章,請檢查 RSS 網址 (HTTP {feed.get('status', '?')})")
        elif newest and newest < cutoff:
            print(f"  ⚠️  {source_name} 最新文章停在 {newest:%Y-%m-%d},來源可能停更或被快取")

    # 依發布時間降冪排序
    all_items.sort(key=lambda x: x["published"], reverse=True)

    output = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "days_back": days_back,
        "total": len(all_items),
        "items": all_items,
    }

    out_path = DATA_DIR / "raw_news.json"
    out_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n✅ 抓取完成,共 {len(all_items)} 則相關新聞")
    print(f"   輸出: {out_path}")


if __name__ == "__main__":
    fetch_all(days_back=7)
