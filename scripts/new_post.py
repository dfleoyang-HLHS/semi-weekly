#!/usr/bin/env python3
"""
new_post.py
快速建立一篇新的週報草稿,自動填入週次與日期。

用法:
  python scripts/new_post.py
  python scripts/new_post.py --week 21 --year 2026
"""

import argparse
from datetime import datetime, date
from pathlib import Path

ROOT = Path(__file__).parent.parent
TEMPLATE = ROOT / "scripts" / "weekly_template.md"
POSTS_DIR = ROOT / "posts"


def get_iso_week(d: date):
    """回傳 ISO 週次 (year, week)"""
    iso = d.isocalendar()
    return iso[0], iso[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", type=int, help="ISO 週次 (預設為本週)")
    parser.add_argument("--year", type=int, help="年份 (預設為本年)")
    parser.add_argument("--draft", action="store_true", help="建立為草稿 (檔名加 draft- 前綴)")
    args = parser.parse_args()

    today = date.today()
    if args.year and args.week:
        year, week = args.year, args.week
    else:
        year, week = get_iso_week(today)

    template = TEMPLATE.read_text(encoding="utf-8")
    content = template.replace("{WEEK_NUMBER}", f"{week:02d}")
    content = content.replace("{YYYY}", str(year))
    content = content.replace("{YYYY-MM-DD}", today.isoformat())

    prefix = "draft-" if args.draft else ""
    filename = f"{prefix}{year}-W{week:02d}-semi-weekly.md"
    out_path = POSTS_DIR / filename

    if out_path.exists():
        print(f"⚠️  檔案已存在: {out_path}")
        return

    out_path.write_text(content, encoding="utf-8")
    print(f"✅ 建立新文章: {out_path}")
    print(f"   下一步: 編輯內容後執行 python scripts/build_index.py")


if __name__ == "__main__":
    main()
