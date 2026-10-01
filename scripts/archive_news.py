#!/usr/bin/env python3
"""
archive_news.py
把每次抓到的新聞 (data/raw_news.json) 併入永久新聞資料庫,避免新聞過期或遺失。

輸出:
  - data/news_archive.json  主資料庫 (依編號排序,網址相同視為同一則)
  - data/news_archive.csv   同內容的 CSV (UTF-8 BOM,可直接用 Excel 開啟)

每則新聞欄位:
  id          永久編號 (流水號,建立後不再變動)
  title       標題
  url         連結
  source      來源
  published   發布日期 (台灣時間 YYYY-MM-DD)
  week        發布週次 (YYYY-WNN)
  summary     內容摘要 (已去除 HTML)
  companies   偵測到的相關公司
  regions     偵測到的相關區域
  first_seen  第一次抓到的日期
  last_seen   最後一次出現在抓取結果的日期

用法:
  python scripts/archive_news.py                 # 併入目前的 data/raw_news.json
  python scripts/archive_news.py --backfill-git  # 從 git 歷史中所有版本的 raw_news.json 補建
"""

import csv
import html
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
RAW_PATH = DATA_DIR / "raw_news.json"
ARCHIVE_JSON = DATA_DIR / "news_archive.json"
ARCHIVE_CSV = DATA_DIR / "news_archive.csv"

sys.path.insert(0, str(Path(__file__).parent))
from generate_news_brief import detect_companies, detect_regions  # noqa: E402

TZ = timezone(timedelta(hours=8))  # 台灣時間
CSV_FIELDS = ["id", "published", "week", "source", "title", "url", "summary",
              "companies", "regions", "first_seen", "last_seen"]


def normalize_url(url):
    """比對用的網址:去掉 #錨點、結尾斜線,https/http 視為相同。"""
    url = url.strip().split("#")[0].rstrip("/")
    return re.sub(r"^http://", "https://", url)


def clean_text(text):
    text = html.unescape(re.sub(r"<[^>]+>", "", text or ""))
    text = re.sub(r"\s*\[(?:…|\.\.\.)\]\s*$", "…", text)  # RSS 的 [&#8230;] 截斷符號
    return re.sub(r"\s+", " ", text).strip()


def to_local_date(iso):
    if not iso:
        return ""
    try:
        return datetime.fromisoformat(iso).astimezone(TZ).date().isoformat()
    except ValueError:
        return iso[:10]


def iso_week(day):
    y, w, _ = datetime.fromisoformat(day).isocalendar()
    return f"{y}-W{w:02d}"


def load_archive():
    if ARCHIVE_JSON.exists():
        return json.loads(ARCHIVE_JSON.read_text(encoding="utf-8"))["items"]
    return []


def merge(archive, raw_items, seen_on):
    """把一批 raw_news 項目併入 archive,回傳新增筆數。"""
    by_url = {normalize_url(a["url"]): a for a in archive}
    next_id = max((a["id"] for a in archive), default=0) + 1
    added = 0
    for it in raw_items:
        url = (it.get("link") or "").strip()
        if not url:
            continue
        key = normalize_url(url)
        if key in by_url:
            rec = by_url[key]
            rec["last_seen"] = max(rec["last_seen"], seen_on)
            rec["first_seen"] = min(rec["first_seen"], seen_on)
            summary = clean_text(it.get("summary"))
            if len(summary) > len(rec["summary"]):  # 保留較完整的摘要
                rec["summary"] = summary
            continue

        title = clean_text(it.get("title"))
        summary = clean_text(it.get("summary"))
        published = to_local_date(it.get("published")) or seen_on
        rec = {
            "id": next_id,
            "title": title,
            "url": url,
            "source": it.get("source", ""),
            "published": published,
            "week": iso_week(published),
            "summary": summary,
            "companies": detect_companies(f"{title} {summary}"),
            "regions": detect_regions(f"{title} {summary}"),
            "first_seen": seen_on,
            "last_seen": seen_on,
        }
        archive.append(rec)
        by_url[key] = rec
        next_id += 1
        added += 1
    return added


def save(archive):
    archive.sort(key=lambda a: a["id"])
    # 一則新聞一行:檔案精簡,且每次更新的 git diff 只會出現新增的那幾行
    rows = ",\n".join("  " + json.dumps(a, ensure_ascii=False) for a in archive)
    ARCHIVE_JSON.write_text(
        "{\n"
        f'"updated_at": "{datetime.now(TZ).isoformat(timespec="seconds")}",\n'
        f'"total": {len(archive)},\n'
        f'"items": [\n{rows}\n]\n'
        "}\n",
        encoding="utf-8",
    )

    with open(ARCHIVE_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for a in archive:
            w.writerow({**a,
                        "companies": "; ".join(a["companies"]),
                        "regions": "; ".join(a["regions"])})


def snapshots_from_git():
    """依時間先後回傳 git 歷史中每個版本的 raw_news.json。"""
    log = subprocess.run(
        ["git", "log", "--reverse", "--format=%H", "--", "data/raw_news.json"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    for sha in log:
        show = subprocess.run(["git", "show", f"{sha}:data/raw_news.json"],
                              cwd=ROOT, capture_output=True, check=True)
        try:
            yield sha[:7], json.loads(show.stdout.decode("utf-8"))
        except json.JSONDecodeError:
            print(f"  ⚠️  {sha[:7]} 的 raw_news.json 無法解析,略過")


def url_to_id():
    """網址 → 資料庫編號,供其他腳本 (如供應鏈圖) 對照。"""
    return {normalize_url(a["url"]): a["id"] for a in load_archive()}


def main():
    archive = load_archive()
    before = len(archive)

    if "--backfill-git" in sys.argv:
        for sha, raw in snapshots_from_git():
            seen_on = to_local_date(raw.get("fetched_at")) or datetime.now(TZ).date().isoformat()
            n = merge(archive, raw.get("items", []), seen_on)
            print(f"  {sha} ({seen_on}): 新增 {n} 則")

    if RAW_PATH.exists():
        raw = json.loads(RAW_PATH.read_text(encoding="utf-8"))
        seen_on = to_local_date(raw.get("fetched_at")) or datetime.now(TZ).date().isoformat()
        merge(archive, raw.get("items", []), seen_on)

    save(archive)
    print(f"✅ 新聞資料庫: 共 {len(archive)} 則 (本次新增 {len(archive) - before} 則)")
    print(f"   {ARCHIVE_JSON.relative_to(ROOT)} / {ARCHIVE_CSV.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
