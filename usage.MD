# 半導體週報系統 — 使用手冊

## 重要網址(收藏到瀏覽器)

- 網站: https://dfleoyang-hlhs.github.io/semi-weekly/
- 管理: https://github.com/dfleoyang-HLHS/semi-weekly
- 通知: https://github.com/dfleoyang-HLHS/semi-weekly/issues
- Claude Pro: https://claude.ai
- NotebookLM (Podcast): https://notebooklm.google.com

## 每週一 — 審閱週報(約 5 分鐘)

週一 06:00 Claude 會自動產生「週報 + 供應鏈圖」並開一個 Pull Request,GitHub 會寄通知信。

1. 開啟 https://github.com/dfleoyang-HLHS/semi-weekly/pulls ,點「📝 2026-WXX 週報待審」
2. 點 Files changed 檢查週報 (`posts/…-semi-weekly.md`) 與供應鏈圖 (`data/supplychain-….json`)
3. 要修改:在該檔案右上角「…」→ Edit file,改完 Commit 到同一個分支
4. 確認無誤 → 按 **Merge pull request** → 約 2 分鐘後網站自動更新 (週報、供應鏈圖、索引一起上線)
5. 不想發佈 → Close pull request

### 一次性設定(只需做一次)
- 到 https://console.anthropic.com 申請 API Key (Claude Pro 訂閱不能用於 API,需另外儲值)
- repo → Settings → Secrets and variables → Actions → New secret,名稱 `ANTHROPIC_API_KEY`
- repo → Settings → Actions → General → Workflow permissions:勾選「Read and write」與「Allow GitHub Actions to create and approve pull requests」

### 手動補跑
- Actions → Semi Weekly and Briefs → Run workflow → mode 選 `weekly` 或 `brief`
- 若 API 失敗,`data/weekly_prompt.md` 仍會產生,可照舊貼到 Claude Pro 手動撰寫

## 每週三、五 — 確認快訊自動產出

- 進 posts/news/,看是否有 YYYY-MM-DD-brief.md
- 不用人工介入

## (可選)Podcast 製作

1. 把週報內容貼到 NotebookLM
2. 點 Audio Overview → Customize → 指定繁體中文兩人對談
3. 下載 m4a
4. 上傳到 Spotify for Podcasters

## 美股報價 (每個交易日盤後自動更新)

- 美股收盤後 (台灣時間週二~六 06:30) 自動抓取「美股追蹤」14 檔的收盤價與漲跌,存到 `data/us_prices.json` 並累積每日收盤價
- 資料來源:Finnhub 免費方案;頁面上方另嵌入 TradingView 官方跑馬燈小工具
- 一次性設定:到 https://finnhub.io 免費註冊取得 API Key,在 repo → Settings → Secrets → Actions 新增 `FINNHUB_API_KEY`
- 手動補跑:Actions → Run workflow → mode 選 `prices`
- 財報指標與近期重點:存在 `data/us_stocks.json`,每週一隨週報由 Claude 依本週新聞更新 (只更新有新資訊的公司),放在週報 PR 中一起審閱
- 新增追蹤公司:同時修改 `scripts/fetch_us_prices.py` 的 WATCHLIST、`data/us_stocks.json` 與 `usstocks.html` 的 TV_SYMBOLS

## 台股報價 (每個交易日盤後自動更新)

- 台股收盤後 (台灣時間週一~五 16:00) 自動抓取「台股追蹤」18 檔收盤價,存到 `data/tw_prices.json` 並累積每日收盤價
- 資料來源:臺灣證券交易所、證券櫃檯買賣中心官方開放資料,免金鑰;報酬率未還原除權息
- 營運指標與近期重點:`data/tw_stocks.json`,每週一隨週報由 Claude 依新聞更新,放在週報 PR 中一起審閱
- 手動補跑:Actions → Run workflow → mode 選 `twprices`
- 新增追蹤公司:修改 `scripts/fetch_tw_prices.py` 的 WATCHLIST 與 `data/tw_stocks.json`,再執行 `python scripts/fetch_tw_prices.py --backfill 13` 補建歷史

## 新聞資料庫

每次抓新聞 (週一、三、五) 都會自動併入永久資料庫,不會因新聞過期而遺失:

- `data/news_archive.json`:主資料庫,一則新聞一行
- `data/news_archive.csv`:同內容,可直接用 Excel 開啟 (UTF-8)
- 欄位:id (永久編號)、published、week、source、title、url、summary、companies、regions、first_seen、last_seen
- 同一網址只存一筆;供應鏈圖的新聞連結也記錄了對應的 id
- 線上網址:https://dfleoyang-hlhs.github.io/semi-weekly/data/news_archive.json

## 常見問題

### 網站沒更新?
- 進 Actions 看 workflow 跑完了沒
- Ctrl+Shift+R 強制清快取

### Workflow 失敗?
- 點失敗的執行,看 prepare 或 deploy 哪一步 ❌
- 看錯誤訊息,通常是網路暫時失敗,過幾小時手動重跑

### 想調整供應鏈圖?
- 每週由 Claude 以上一期為基礎自動增修 `data/supplychain-YYYY-WNN.json`,在 PR 中審閱
- 手動修改:直接編輯該週 JSON 的 nodes / edges;週次索引 `supplychain-index.json` 會自動重建

## 系統架構

- 前端: HTML + CSS + JS(純靜態)
- 部署: GitHub Pages + GitHub Actions
- 內容: Markdown + YAML front matter
- 索引: Python 自動掃描 posts/ 產生 db.json
- 主題: localStorage + CSS variables
