#!/usr/bin/env python3
"""
build_index.py
掃描 posts/ 資料夾的所有 Markdown 文章,
解析 YAML front matter,產生:
  - data/db.json       (所有文章主索引)
  - data/companies.json (依公司聚合)
  - data/tags.json      (標籤雲)
  - data/regions.json   (依區域聚合)
"""

import os
import re
import json
import yaml
from datetime import datetime
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
POSTS_DIR = ROOT / "posts"
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)


def parse_front_matter(content):
    """解析 Markdown 開頭的 YAML front matter"""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return None, content
    try:
        meta = yaml.safe_load(match.group(1))
        body = match.group(2)
        return meta, body
    except yaml.YAMLError as e:
        print(f"YAML 解析錯誤: {e}")
        return None, content


def extract_summary(body, max_len=200):
    """若沒有 summary 欄位,自動從內文取前 200 字"""
    text = re.sub(r"^#+ .*$", "", body, flags=re.MULTILINE)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_len] + ("..." if len(text) > max_len else "")


def build_index():
    articles = []
    companies_map = defaultdict(list)
    tags_map = defaultdict(list)
    regions_map = defaultdict(list)

    for md_file in sorted(POSTS_DIR.glob("*.md")):
        # 跳過草稿
        if md_file.name.startswith("draft-"):
            continue

        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        meta, body = parse_front_matter(content)
        if not meta:
            print(f"⚠️  跳過 (無 front matter): {md_file.name}")
            continue

        slug = md_file.stem
        article = {
            "slug": slug,
            "filename": md_file.name,
            "title": meta.get("title", slug),
            "date": str(meta.get("date", "")),
            "week": meta.get("week", ""),
            "category": meta.get("category", "未分類"),
            "regions": meta.get("regions", []),
            "companies": meta.get("companies", []),
            "tags": meta.get("tags", []),
            "summary": meta.get("summary") or extract_summary(body),
            "cover_image": meta.get("cover_image", ""),
            "word_count": len(body),
        }
        articles.append(article)

        # 反向索引
        for c in article["companies"]:
            companies_map[c].append(slug)
        for t in article["tags"]:
            tags_map[t].append(slug)
        for r in article["regions"]:
            regions_map[r].append(slug)

    # 依日期降冪排序
    articles.sort(key=lambda x: x["date"], reverse=True)

    # 寫出主索引
    db = {
        "generated_at": datetime.now().isoformat(),
        "total": len(articles),
        "articles": articles,
    }
    (DATA_DIR / "db.json").write_text(
        json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 公司聚合 (含計次)
    companies = [
        {"name": name, "count": len(slugs), "articles": slugs}
        for name, slugs in sorted(
            companies_map.items(), key=lambda x: len(x[1]), reverse=True
        )
    ]
    (DATA_DIR / "companies.json").write_text(
        json.dumps(companies, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 標籤雲
    tags = [
        {"name": name, "count": len(slugs), "articles": slugs}
        for name, slugs in sorted(
            tags_map.items(), key=lambda x: len(x[1]), reverse=True
        )
    ]
    (DATA_DIR / "tags.json").write_text(
        json.dumps(tags, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 區域聚合
    regions = [
        {"name": name, "count": len(slugs), "articles": slugs}
        for name, slugs in sorted(
            regions_map.items(), key=lambda x: len(x[1]), reverse=True
        )
    ]
    (DATA_DIR / "regions.json").write_text(
        json.dumps(regions, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"✅ 索引建立完成")
    print(f"   文章數: {len(articles)}")
    print(f"   公司數: {len(companies)}")
    print(f"   標籤數: {len(tags)}")
    print(f"   區域數: {len(regions)}")


if __name__ == "__main__":
    build_index()
