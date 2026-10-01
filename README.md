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
│   ├── tags.json           # 標籤雲
│   ├── news_archive.json   # 新聞資料庫 (永久保存,每次抓取自動累積)
│   └── news_archive.csv    # 同上,CSV 格式 (可用 Excel 開啟)
│
├── scripts/                # 自動化腳本
│   ├── build_index.py      # 掃描 posts/ 產生 db.json
│   ├── fetch_news.py       # 抓取 RSS 與新聞來源
│   ├── archive_news.py     # 新聞併入永久資料庫
│   ├── fetch_us_prices.py  # 美股盤後報價 (Finnhub)
│   ├── fetch_tw_prices.py  # 台股盤後報價 (證交所、櫃買中心開放資料)
│   ├── generate_draft.py   # 呼叫 Claude API 生成草稿
│   ├── verify_weekly.py    # 週報自動查核 (格式、連結、事實)
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

## 每週工作流程 (台灣時間)

| 時間 | 動作 | 是否需人工 |
|---|---|---|
| 週一 06:00 | 抓新聞 → Claude 產生週報、供應鏈圖、個股卡片 → 自動查核 → 開 Pull Request | 查核未通過時才需處理 |
| 週一 20:00 | 自動 Merge 查核通過的週報 PR → 重建索引 → 部署 | 否 (可加 `hold` 標籤暫停) |
| 週三、五 06:00 | 抓新聞 → 產生快訊 → 部署 | 否 |
| 週二~六 06:30 | 美股收盤後抓取報價 → 部署 | 否 |
| 週一~五 16:00 | 台股收盤後抓取報價 → 部署 | 否 |

詳細操作見 `usage.MD`。需在 repo Secrets 設定 `ANTHROPIC_API_KEY`。

## 部署

純靜態網站,直接部署到 GitHub Pages,無後端需求。
