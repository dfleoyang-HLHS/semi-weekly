# 半導體週報系統 — 使用手冊

## 重要網址(收藏到瀏覽器)

- 網站: https://dfleoyang-hlhs.github.io/semi-weekly/
- 管理: https://github.com/dfleoyang-HLHS/semi-weekly
- 通知: https://github.com/dfleoyang-HLHS/semi-weekly/issues
- Claude Pro: https://claude.ai
- NotebookLM (Podcast): https://notebooklm.google.com

## 每週一 — 撰寫週報(15-20 分鐘)

1. 早上開啟 Issues,看到「2026-WXX 週報待撰寫」
2. 點進去,複製 weekly_prompt.md 內容(點 Raw → Ctrl+A → Ctrl+C)
3. 開 Claude Pro 新對話,貼上,送出
4. 等 1-2 分鐘,複製 Claude 完整回覆
5. 進 repo 的 posts/ 資料夾,Add file → Create new file
6. 檔名:2026-WXX-semi-weekly.md
7. 貼上內容,Commit
8. 關閉 Issue

## 每週三、五 — 確認快訊自動產出

- 進 posts/news/,看是否有 YYYY-MM-DD-brief.md
- 不用人工介入

## (可選)Podcast 製作

1. 把週報內容貼到 NotebookLM
2. 點 Audio Overview → Customize → 指定繁體中文兩人對談
3. 下載 m4a
4. 上傳到 Spotify for Podcasters

## 常見問題

### 網站沒更新?
- 進 Actions 看 workflow 跑完了沒
- Ctrl+Shift+R 強制清快取

### Workflow 失敗?
- 點失敗的執行,看 prepare 或 deploy 哪一步 ❌
- 看錯誤訊息,通常是網路暫時失敗,過幾小時手動重跑

### 想加新公司到供應鏈圖?
- 編輯 supplychain.html,在對應層級加新的 <rect> + <text>
- 加連線:用 <line> 或 <path>

## 系統架構

- 前端: HTML + CSS + JS(純靜態)
- 部署: GitHub Pages + GitHub Actions
- 內容: Markdown + YAML front matter
- 索引: Python 自動掃描 posts/ 產生 db.json
- 主題: localStorage + CSS variables
