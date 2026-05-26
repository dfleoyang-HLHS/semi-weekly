# 半導體 + AI 供應鏈週報 (Semi-Weekly)

每週固定產出半導體與 AI 供應鏈產業分析的網站,部署於 GitHub Pages。

## 專案架構

```
semi-weekly/
├── index.html              # 首頁:最新報告與文章列表
├── article.html            # 單篇文章閱讀頁
├── company.html            # 公司頁面:聚合該公司所有提及
├── timeline.html           # 產業時間軸視覺化
├── search.html             # 搜尋與篩選
│
├── posts/                  # 所有文章 (Markdown + YAML front matter)
│   ├── 2026-W21-cowos-weekly.md
│   └── ...
│
├── data/                   # 自動產生的索引檔
│   ├── db.json             # 主索引
│   ├── companies.json      # 公司聚合
│   └── tags.json           # 標籤雲
│
├── scripts/                # 自動化腳本
│   ├── build_index.py      # 掃描 posts/ 產生 db.json
│   ├── fetch_news.py       # 抓取 RSS 與新聞來源
│   ├── generate_draft.py   # 呼叫 Claude API 生成草稿
│   ├── new_post.py         # 手動建立新文章模板
│   └── weekly_template.md  # 週報固定模板
│
├── assets/                 # CSS, JS, 圖片
│   ├── style.css
│   └── app.js
│
└── .github/workflows/
    └── weekly.yml          # 每週一自動執行
```

## 每週工作流程

**自動部分 (每週一 06:00 自動執行):**
1. GitHub Actions 觸發 `fetch_news.py`,抓取過去 7 天的 RSS 來源
2. 呼叫 Claude API 生成初稿 (`generate_draft.py`)
3. 草稿存到 `posts/draft-YYYY-WNN.md`,等待人工審閱

**人工部分 (每週一早上花 30 分鐘):**
1. 開啟 draft,確認內容、補上財報數字與圖表
2. 改名為正式檔名 (移除 `draft-` 前綴)
3. `git commit && git push` → GitHub Actions 自動重建索引並部署

## 部署

純靜態網站,直接部署到 GitHub Pages,無後端需求。
