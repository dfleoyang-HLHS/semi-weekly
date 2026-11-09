---
title: "半導體 + AI 供應鏈週報 (2026-W46)"
date: "2026-11-09"
week: "2026-W46"
category: "週報"
regions: ["美國", "台灣", "日本", "韓國", "中國大陸", "歐洲"]
companies:
  - NVIDIA
  - AMD
  - Marvell
  - Lumentum
  - Qualcomm
  - Intel
  - Microsoft
  - Oracle
  - Google
  - Meta
  - Apple
  - OpenAI
  - Anthropic
  - Nscale
  - Tesla
  - SpaceX
  - Terafab
  - Micron
  - GlobalFoundries
  - Arm
  - TSMC
  - MediaTek
  - Winbond
  - Phison
  - Unimicron
  - KYEC
  - PTI
  - Vanguard
  - King Slide
  - Foxconn
  - Rohm
  - Nittobo
  - JX Advanced Metals
  - Samsung
  - SK Hynix
  - Naver
  - FuriosaAI
  - JNTC
  - Hua Hong
  - CXMT
  - Moonshot AI
  - Infineon
tags: ["美國期中選舉", "資料中心監管", "費半單日崩 12%", "台股史上最大盤中跌點", "黃仁勳間諜疑雲", "H200 卡關香港", "台積電傳布局 3D DRAM", "Marvell 併 Lumentum", "記憶體長約", "HBM4 良率"]
summary: "民主黨在期中選舉拿下國會兩院,德州新州長擬暫停核准新資料中心,10 州 41 項資料中心地方公投有 40 項傾向限制,市場擔憂 AI 基建放緩,費半 11 月 5 日崩跌 12.25%、輝達市值單日蒸發 4,470 億美元,台股隔日盤中最多跌逾 3,700 點創史上最大盤中跌點。黃仁勳坦承與涉嫌中國間諜的 Megaspeed 前高層有婚外情,NVIDIA 董事會啟動獨立調查。產業面,Marvell 以全股票約 1,150 億美元收購 Lumentum,台積電傳應 NVIDIA 要求研擬 3D DRAM,華邦電 10 月營收年增 256.96%。"
cover_image: ""
---

## 本週重點

本週主軸是「選舉結果讓 AI 基建從財務疑慮轉向政策風險」。民主黨拿下美國國會兩院,預計 2027 年 1 月正式掌握國會主導權 [8];11 月 3 日全美 10 州共 41 項資料中心相關地方公投,其中 40 項傾向限制開發 [213],德州當選州長 Gina Hinojosa 宣布將暫停資料中心開發措施並重審可能涉及 SpaceX 的土地交易 [98]。高盛估美國約 45% 規劃中擴建容量受民主黨州政策限制,德州單獨占 25% [225]。11 月 5 日美股全面下殺,道瓊跌 1,833 點、那指跌 5.52%、費半崩 12.25%,輝達市值單日蒸發 4,470 億美元 [215],費半創疫情以來最差單日表現 [228];台股 6 日開盤跌逾 8%,盤中最多跌逾 3,700 點、創史上最大盤中跌點,台積電一度亮跌停 [161]。週五晶片股反彈,費半勁揚 4.21%,但那指、標普周線仍四連黑 [91]。同時,黃仁勳坦承婚外情並向家人與員工道歉,NVIDIA 董事會已啟動獨立調查 [1][34],事件從私生活延伸到國安、出口管制與公司治理 [3]。產業面供需仍緊:Marvell 以全股票、約 1,150 億美元收購 Lumentum [178],台積電傳應 NVIDIA 要求研擬 3D DRAM 生產計畫 [81],華邦電 10 月營收年增 256.96% [141]。

---

## 一、產業全貌

**主軸一:期中選舉把「資料中心能不能蓋」變成新變數。** CNBC 調查顯示 56% 選民把 AI 與資料中心列為投票關鍵,參議員桑德斯呼籲全美暫停興建資料中心;德州占全美規劃中資料中心產能 27% [214]。高盛估德州約 13GW 資料中心容量曝險 [225],瑞銀估美國 2028 年新增資料中心容量約 30% 恐有停建風險 [177]。彭博點名德州、俄亥俄州、喬治亞州與賓州四大資料中心重鎮可能收緊新案 [128]。國會方面,兩黨協商提案擬維持 AI 晶片出口限制 18 個月,中國只能取得落後美國最先進產品兩個世代的技術 [87];民主黨也擬傳喚 NVIDIA 等矽谷巨頭出席聽證 [82]。業者因應方式分歧:OpenAI 承諾自有園區全額負擔用電與供電設施成本 [89],Google 仍宣布投資 170 億美元在懷俄明州興建資料中心,搭配 Bloom Energy 供應的 702MW 燃料電池電廠 [50];NVIDIA 傳洽談把 Brightspeed 在美國 20 州、130 多棟舊電信大樓改造為小型 AI 資料中心,以避開新建案的嚴格審批 [146]。

**主軸二:算力買方開始挑剔,融資與新雲端壓力升高。** 微軟傳不再續約向甲骨文租用的 AI 算力,原因是伺服器採用舊世代 NVIDIA 晶片,並重審與 CoreWeave 等外部算力合作,承諾總額逾 800 億美元 [88];微軟也放棄行使在德州擴大向 Nscale 租用算力的選擇權,讓 Nscale 規劃中的 350 億美元 IPO 增添變數 [179]。甲骨文合約積壓 6,640 億美元,OpenAI 傳重新評估明年資料中心容量 [92]。高盛指超大科企今年已發債 2,960 億美元,資料中心 CDS 突破 500 基點 [45];SpaceX 五年期 CDS 利差飆至 284.3 個基點創新高 [164]。另一方面需求數字仍強:Anthropic 截至 10 月底年化營收 (ARR) 突破 800 億美元 [85],Meta 首發 90 億歐元債券,認購需求達 530 億歐元 [241]。

**主軸三:記憶體荒延伸到「誰來做記憶體」。** Counterpoint 統計第三季全球 DRAM 營收年增 369%、逼近 2,000 億美元,一般 DDR 與 LPDDR 成長快於 HBM [100]。台積電傳應 NVIDIA 要求研擬 3D DRAM 生產計畫,評估新建晶圓廠或收購既有廠房改造,台積電與 NVIDIA 均未回應 [81];華邦電董事長焦佑鈞則表示,台積電與三大記憶體原廠均有合作、不會加入競爭 [67]。高通完成 HBC 記憶體架構初步硬體驗證,定位為 HBM4 的低成本替代方案 [121]。

---

## 二、美國 (USA)

### NVIDIA
- 《金融時報》報導美國政府情報備忘錄指稱,黃仁勳曾與新加坡 Megaspeed 高階主管黃樂 (Alice Huang) 發展戀愛關係,相關報導指黃樂涉嫌向中國政府提供情報 [32][134];黃仁勳 8 日發出道歉信,董事會宣布啟動獨立調查,釐清他是否成為外國情報單位鎖定的目標 [34]。川普表示黃仁勳應繼續擔任執行長 [36];三名美國議員要求黃仁勳出席閉門會議說明 [134]。
- 約 60 萬顆 H200 存放在香港等待進入中國,北京尚未批准大規模進口 [105];阿里巴巴、騰訊、字節跳動等共訂購約 600 萬顆 RTX Pro 5500,未來 4 個月預計只能收到約 1% [244]。
- 11 月 5 日股價跌 9.3% [152];週五反彈,晶片股自六年來最慘烈拋售後強彈 [85]。
- DIGITIMES Research 估第四季全球伺服器出貨 489 萬台、季增 5.5%,但 Vera Rubin 存在供應問題 [18];供應鏈指 Vera Rubin 出貨將於 2027 年第一季逐步拉升,ASIC 伺服器填補空檔 [232]。
- 傳將南韓 JNTC 列入採購供應商名單,採購玻璃通孔 (TGV) 基板付費樣品 [125];力推 PTFE 無玻纖布方案,PCB 大廠審慎評估 [38]。

### AMD / Marvell / Qualcomm
- **AMD**:第三季營收 134 億美元,資料中心營收年增 97% 至 85 億美元,占比升至 64% [7];與南韓 FuriosaAI、MangoBoost 簽約,2027 年春季前在首爾打造異質 AI 運算叢集 [223];Naver Cloud 已在約 3.5 萬台伺服器使用 EPYC [242]。南韓 Moreh 稱在其測試中 MI355X 推論吞吐量逾 B200 兩倍 [243]。
- **Marvell**:11 月 2 日宣布以全股票、約 1,150 億美元收購 Lumentum,須經監管批准,預計 2028 年上半年完成 [178]。
- **Qualcomm**:2026 會計年度第 4 季手機晶片營收年減 26%,目標 2027 會計年度資料中心營收 50 億美元、2029 會計年度 150 億美元 [246];財測不如預期,股價跌 9% [171];AI250 樣品目標 2027 年上半年 [121]。Alphabet 第三季買進高通股票,持股價值近 5.48 億美元 [84]。

### Microsoft / Oracle / Google / Meta / Apple
- **Microsoft**:傳對新雲端業者態度轉趨保守,加強監督 IREN、Nebius 及 Nscale 等夥伴的建置進度 [107]。
- **Oracle**:2026 財年資本支出 557 億美元,2027 財年估 900 億至 950 億美元 [92];雲端業務營收 180 億美元,自由現金流轉負 [88]。
- **Google**:第三季資本支出 513.6 億美元,連兩季自由現金流為負 [50];2027 至 2028 年將投入 150 億美元擴大馬來西亞資料中心與雲端布局 [198]。
- **Meta**:收購 AI 程式開發新創 Conductor,未公開金額 [195];總裁 Dina Powell McCormick 表示資料中心已成選舉關鍵議題 [111]。
- **Apple**:逾一年來首度發行投資等級公司債,籌約 70 億美元 [197];晨星稱 10 月底蘋果已取代 NVIDIA,重登美國總市場指數市值第一 [147]。

### Tesla / SpaceX / Terafab / OpenAI / Anthropic
- **Tesla**:公布 AI 晶片藍圖,SI6 預計 2029 至 2030 年推出、運算效能達 HW4 的 80 倍;Dojo D3 重新啟動並導入 HBM;SI5 由台積電、三星以 3 奈米 / 2 奈米生產,三星也將代工 SI6 至 2033 年 [68]。Cybertruck 將於明年年中左右逐步停產 [51]。
- **SpaceX**:持有 899 億美元現金、負債 380 億美元,第三季資本支出 164.4 億美元 [164];特斯拉與 SpaceX 兩日市值合計蒸發約 4,560 億美元 [216]。
- **Terafab**:馬斯克稱目標每年 1 太瓦產能,StarMind 太空運算設備最快 2027 年第三季發射 [41]。
- **OpenAI**:財務長 Friar 表示會繼續投資 AI 資料中心並持續募資 [89];11 月 5 日發布政策藍圖,承諾不與地方官員簽保密協議並讓社區參與討論 [108]。
- **Anthropic**:據 DIGITIMES 週末速寫,IPO 估值下修至 1.3 兆美元 [53]。

### Intel / GlobalFoundries / Arm
- **Intel**:強調 EMIB 封裝將迎接 AI 晶片大面積化商機 [218];DIGITIMES 分析師指英特爾 18A 製程轉回 Intel 3,產能調度吃緊 [114]。
- **GlobalFoundries**:第三季營收 18.99 億美元、年增 13%,智慧行動裝置業務年減 19% [250]。
- **Arm**:最新營收展望僅略高於市場預期,AI 資料中心展望仍待驗證 [238]。

### 總經
- 10 月非農就業增加 16.5 萬人、失業率降至 4.1%,美債 10 年期殖利率升至 4.86% [91];市場估 12 月再升息 1 碼機率 79% [64]。週二公布 10 月 CPI [90]。

---

## 三、台灣 (Taiwan)

### 台積電 TSMC (2330.TW)
- 傳應 NVIDIA 要求研擬 3D DRAM 生產計畫,由徐國晉主導,投產時程尚未明朗 [81]。
- 傳德州政府收到一項 450 億美元、興建兩座先進晶圓廠的未具名企業投資案,目標 2029 年底前量產 [150];台積電傳鎖定北德州謝爾曼作為美國第二座大型生產據點 [19]。
- 11 月 6 日一度亮跌停,貢獻台股逾 1,500 點跌點 [161]。

### 記憶體 (華邦電、群聯)
- **華邦電**:10 月營收 293.61 億元、年增 256.96% [141];董事會通過約 731 億元資本支出擴建高雄廠,並將選擇 10 家策略客戶簽 2029 至 2032 年長約 [235]。焦佑鈞稱 2027 至 2028 年記憶體需求明確,下一波循環預計 2029 年開始 [57],記憶體漲價已到極限 [60];員工獎金平均可望達約 30 個月 [66]。
- **群聯**:第三季營收 860.76 億元、毛利 513.8 億元、EPS 138 元,均創同期新高;AI 業務貢獻突破 5 成 [137]。

### 封測、載板與晶圓代工 (京元電、力成、欣興、世界先進)
- **京元電**:10 月營收 44.26 億元、年增 29.47% [131];FactSet 目標價中位數下修至 330 元 [148];張高薰表示赴美設廠計畫如期推進 [80]。
- **力成**:10 月營收 87.27 億元、年增 25.2% [139]。
- **欣興**:10 月營收 189.86 億元、年增 67.62% [138]。
- **世界先進**:第三季營收 157.02 億元、季增 10.2%、年增 27.2%,第四季稼動率逾 9 成 [142];VSMC 新加坡 12 吋廠的中介層估占 VSMC 營收 5 成 [143]。

### IC 設計與系統 (聯發科、川湖、鴻海)
- **聯發科**:傳延攬前英特爾高層 Navid Shahriari 於 11 月 9 日出任資深副總,推進 CoWoS 與 EMIB 雙軌策略 [224];副總經理侯上勇稱 CoWoS「從有趣變得頭痛」,卡位封裝產能成當務之急 [133]。
- **川湖**:2026 年第三季稼動率降至六成,但 2026 與 2027 年毛利率仍估維持 85% 以上,2027 上半年 Vera Rubin 量產後高階導軌需求將明顯成長 [37]。
- **鴻海**:展示 NVIDIA DSX POD 貨櫃式方案,延伸至資料中心系統整合 [199]。

### 美光台灣與政策
- 彭博報導美光因勞資糾紛未解,暫停桃園工廠計畫 [155];供應鏈證實暫緩桃園無塵室工程,但 EUV 設備訂單未變 [182]。
- 晶創方案 2027 年新增先進記憶體計畫 [203]。

---

## 四、日本 (Japan)

### Rohm / 日東紡 / JX 金屬
- **Rohm**:上修 2026 年度財測,合併淨利由 290 億日圓提高至 450 億日圓,扭轉 2025 年度 1,584 億日圓虧損 [112]。
- **日東紡**:投資約 200 億日圓擴產 T 玻璃纖維布 [106]。
- **JX 金屬**:將 AI 晶片用高純度硫酸銅產能提高至 2026 年度上半水準的 1.5 倍 [109]。
- **三菱重工**:投資 4.9 億美元擴建美國喬治亞州燃氣渦輪工廠 [23]。

---

## 五、韓國 (South Korea)

### SK Hynix (000660.KS)
- HBM4 良率傳已達 60% 中段、居業界之冠,得以在產能集中於 HBM 時仍擴大伺服器 DRAM 供應 [236]。
- 美國 AI 投資法人 HYAICO 以 3.7716 億美元向 SK Telecom 關係企業取得 Penguin Solutions 股權 [104];子公司 Solidigm 評估在美國興建 NAND 晶圓廠,資金與時程未定 [70]。

### Samsung Electronics (005930.KS)
- 平澤 P5 第 2 座晶圓廠預計 2027 年 1 月啟動結構工程,因應短缺預期延續至 2028 年 [113]。
- 傳將在器興園區興建 2 奈米與 4 奈米級晶圓代工廠,擴大 HBM 邏輯 base die 產能,估投資 25 兆韓元 [237]。
- 傳將已關閉的 8 吋 S7 廠約 300 台設備出售給 DB 集團 [69]。

### Naver / FuriosaAI / 南韓 SSD
- **Naver**:與 Brookfield 簽訂最高 90 億美元基礎設施協議,準備推出 NVIDIA 支持的 AI 工廠業務 [227]。
- 南韓 SSD 出口暴增 584%,三星、SK 海力士擴大企業級 SSD 布局 [101]。

---

## 六、中國大陸 (China)

### 華虹 / 長鑫
- **華虹宏力**:第三季營收 67.06 億元人民幣、年增 13.95% [116],獲利增 147.1%,並擴展矽光子與電源管理晶片 [97]。
- **長鑫存儲**:預付款激增 16 倍,主流 DRAM 吃緊有助市占擴大 [233];阿里巴巴、騰訊、字節跳動傳搶簽南韓記憶體長約 [183]。

### 算力取得
- 月之暗面傳透過歐洲新雲端業者遠端租用 NVIDIA Blackwell 算力 [127];美方延伸管制海外算力,擠壓東南亞資料中心業者 [240]。

---

## 七、歐洲 (Europe)

### Infineon / Nscale / Aumovio
- **英飛凌**:看好 800V 直流架構、固態變壓器與垂直供電,以 Si、SiC、GaN 產品組合布局 AI 基礎設施 [26]。
- **Nscale**:規劃 350 億美元 IPO,但微軟傳放棄擴大德州算力租約 [179]。
- **Aumovio**:示警資料中心需求將推動 2027 年半導體價格大幅上漲 [11]。
- 德國 QuantumDiamonds 以量子感測技術測試 HBM 的 TSV 缺陷 [234]。

---

## 八、本週財報與營收重點

| 公司 | 期別 | 營收 | YoY | 重點 |
|------|------|------|------|------|
| AMD | 3Q26 | 134 億美元 | 待確認 | 資料中心 85 億美元 (+97%) [7] |
| GlobalFoundries | 3Q26 | 18.99 億美元 | +13% | 智慧行動裝置 -19% [250] |
| 群聯 | 3Q26 | 860.76 億元 | 待確認 | EPS 138 元;AI 業務逾 5 成 [137] |
| 世界先進 | 3Q26 | 157.02 億元 | +27.2% | Q4 稼動率逾 9 成 [142] |
| 華虹宏力 | 3Q26 | 67.06 億元人民幣 | +13.95% | 獲利 +147.1% [116][97] |
| 華邦電 | 10 月 | 293.61 億元 | +256.96% | 擴建高雄廠約 731 億元 [141][235] |
| 欣興 | 10 月 | 189.86 億元 | +67.62% | 1-10 月 +40.88% [138] |
| 力成 | 10 月 | 87.27 億元 | +25.2% | 1-10 月 +29.75% [139] |
| 京元電 | 10 月 | 44.26 億元 | +29.47% | 1-10 月 +33.52% [131] |
| Rohm | 2026 年度財測 | 待確認 | 待確認 | 淨利上修至 450 億日圓 [112] |

---

## 九、風險與下週觀察點

1. **美國 10 月 CPI (週二)**:是否推升 Fed 12 月升息預期 [90][64]。
2. **CoreWeave、Nebius、思科、應材財報**:CoreWeave 須交代擴張籌資與借款成本 [65]。
3. **NVIDIA 董事會獨立調查與國會說明**:調查進度、閉門會議安排,以及民主黨推動的出口管制法案 [3][134][87]。
4. **各州資料中心審批**:德州暫停令細節,以及俄亥俄、喬治亞、賓州是否跟進 [98][128]。
5. **台積電 3D DRAM 與德州投資傳聞**:是否獲公司證實 [81][150]。
6. **H200 對中出貨**:香港約 60 萬顆庫存能否獲北京放行 [105]。

---

## 資料來源

- [1] [黃仁勳認共諜婚外情！道歉信全文曝光](https://news.cnyes.com/news/id/6652585) — 鉅亨網
- [3] [黃仁勳涉間諜疑雲引爆NVIDIA治理危機 董事會發獨立調查聲明](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000774010_AQG1GP660AEJYO15UM4WH) — DigiTimes
- [7] [【漫圖秒懂】超微資料中心營收狂飆97% 跟上NVIDIA成長腳步](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773681_5VA5O7J19HWFOS0LRPV0N) — DigiTimes
- [8] [美國期中選舉恐改寫AI競爭格局 中國出口迎轉機](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773869_75A7W6F37Q8SFM80BMXJM) — DigiTimes
- [11] [德國汽車零件供應商：資料中心建置潮續推2027半導體價](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773833_GGB9GJW62KEVME4PW5BWQ) — DigiTimes
- [18] [4Q26伺服器出貨續強 Vera Rubin供應受限、Arm架構CPU成主角](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773412_J7V5RJCA07H0XM3C7DPA6) — DigiTimes
- [19] [【動物農莊】鴿們聊兩大晶圓代工巨頭都到德州 先開打的是人才戰？](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773568_61J4UMO47PFDP57QSVQZ7) — DigiTimes
- [23] [三菱重工4.9億美元擴建美國燃氣渦輪廠 瞄準AI電力需求](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773686_4HD5N3929QJ4335C8HYZW) — DigiTimes
- [26] [AI供電邁向800V直流 英飛凌以三大材料組合布局電網至晶片商機](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773733_FJI81YP12MWXFG4LIXN6D) — DigiTimes
- [32] [黃仁勳突發公開信坦承婚外情 NVIDIA捲中國間諜疑雲、董事會啟動獨立調查](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000774009_KQXLSGHF10ULOS843L4Y7) — DigiTimes
- [34] [黃仁勳出軌！坦承共諜婚外情 向妻子道歉](https://news.cnyes.com/news/id/6652534) — 鉅亨網
- [36] [黃仁勳認了婚外情 川普挺留任輝達CEO「他是很好的人」](https://news.cnyes.com/news/id/6652546) — 鉅亨網
- [37] [川湖迎Vera Rubin量產與周邊機櫃導入導軌 2027年獲利動能看俏](https://news.cnyes.com/news/id/6651767) — 鉅亨網
- [38] [輝達力推 PTFE 無玻纖布方案，材料商搶卡位、PCB 大廠審慎評估](https://technews.tw/2026/11/08/materials-suppliers-rush-to-develop-glass-free-ptfe-laminates/) — TechNews
- [41] [馬斯克揭特斯拉、SpaceX未來布局！太空AI資料中心、Terafab晶圓廠與Optimus機器人全曝光](https://news.cnyes.com/news/id/6652258) — 鉅亨網
- [45] [1998還是2000？高盛：AI股暴跌更像LTCM危機而非網路泡沫化 但最大疑問仍是投資回報](https://news.cnyes.com/news/id/6651832) — 鉅亨網
- [50] [AI支出疑慮升高之際 Google現金流連兩季轉負 仍砸170億美元建資料中心](https://news.cnyes.com/news/id/6651952) — 鉅亨網
- [51] [特斯拉Cybertruck將逐步停產！馬斯克押注AI轉型 背後是電動皮卡銷售困境](https://news.cnyes.com/news/id/6651843) — 鉅亨網
- [53] [週末新聞速寫：傳台積電擬布局生產3D DRAM | 美方認定中國女間諜接近黃仁勳 | Anthropic IPO估值下修至1.3兆美元](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773980_JYR8HKJ49GX0JZLAGTJO8) — DigiTimes
- [57] [焦佑鈞：2027~2028 年記憶體需求明確，下一波循環預計 2029 年開始](https://finance.technews.tw/2026/11/07/winbond-believes-that-memory-demand-will-be-strong-in-2027-2028/) — TechNews
- [60] [焦佑鈞：記憶體漲價已到極限，不希望景氣下行時間太晚來](https://finance.technews.tw/2026/11/07/memory-price-increases-have-reached-their-limit/) — TechNews
- [64] [美期中選舉重塑Fed政策空間！華許升息阻力降低 但經濟可能不再需要更高利率](https://news.cnyes.com/news/id/6651852) — 鉅亨網
- [65] [反彈恐是死貓跳？財經名嘴示警AI融資疑慮未除 CoreWeave、Nebius下周財報是關鍵考驗](https://news.cnyes.com/news/id/6651844) — 鉅亨網
- [66] [華邦電 2026 年業績亮眼，員工獎金平均可望達到約 30 個月](https://finance.technews.tw/2026/11/07/winbond-electronics-employees-are-expected-to-receive-an-average-bonus-of-approximately-30-months-salary/) — TechNews
- [67] [傳跨足先進記憶體生產？焦佑鈞：台積電與三大記憶體原廠均有合作不會加入競爭](https://finance.technews.tw/2026/11/07/tsmc-collaborates-with-all-three-major-memory-manufacturers-and-will-not-join-the-competition/) — TechNews
- [68] [特斯拉AI晶片藍圖曝光！Dojo D3導入HBM、SI6效能拚提升80倍、採2奈米製程](https://news.cnyes.com/news/id/6652054) — 鉅亨網
- [69] [Samsung reportedly sells 300 chipmaking tools to DB Group](https://www.digitimes.com/news/a20261106VL218/samsung-equipment-manufacturing-production-capacity-production.html) — DigiTimes Asia
- [70] [Solidigm eyes US NAND fab as funding questions linger](https://www.digitimes.com/news/a20261106PD229/solidigm-fab-nand-flash-nand-funding.html) — DigiTimes Asia
- [80] [美期中選舉變天牽動AI投資？ 京元電張高薰：赴美設廠計畫如期推進](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773874_9KK7BM038EA64W3HWBHL7) — DigiTimes
- [81] [台積電要做AI記憶體？傳應輝達要求研擬生產3D DRAM](https://news.cnyes.com/news/id/6651567) — 鉅亨網
- [82] [美國會換人掌權 輝達AI晶片出口將成審查焦點、對中生意再添變數](https://news.cnyes.com/news/id/6651657) — 鉅亨網
- [84] [Google母公司買進高通！持股價值近5.48億美元](https://news.cnyes.com/news/id/6651143) — 鉅亨網
- [85] [輝達、AMD強彈！兩大利多帶動晶片股反攻 分析師提醒「繫好安全帶」](https://news.cnyes.com/news/id/6651674) — 鉅亨網
- [87] [輝達哪些AI晶片還能賣中國？美國會擬設「落後兩代」門檻 H200剛好踩線](https://news.cnyes.com/news/id/6651713) — 鉅亨網
- [88] [微軟傳不再續約 逐步停用向甲骨文租用的AI算力](https://news.cnyes.com/news/id/6651736) — 鉅亨網
- [89] [美國選民踩煞車 OpenAI還會蓋資料中心？財務長：會繼續投資](https://news.cnyes.com/news/id/6651732) — 鉅亨網
- [90] [AI股跌夠了嗎？美股下周兩大考驗：CPI看升息、CoreWeave看資金](https://news.cnyes.com/news/id/6651165) — 鉅亨網
- [91] [〈美股盤後〉晶片股反彈！費半勁揚逾4.2% 台積電ADR升超6% 那指標普周線四連黑](https://news.cnyes.com/news/id/6651785) — 鉅亨網
- [92] [AI資料中心熱潮出現裂縫？微軟不續租甲骨文AI算力 6640億美元合約積壓曝險 兩檔ETF成觀察焦點](https://news.cnyes.com/news/id/6651829) — 鉅亨網
- [97] [Hua Hong Grace eyes silicon photonics expansion as AI chip shortages lift pricing power](https://www.digitimes.com/news/a20261106VL204/photonics-silicon-expansion-revenue-demand.html) — DigiTimes Asia
- [98] [德州新州長擬暫停資料中心開發 SpaceX土地交易也要重審](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773800_TUZ9BOHNLTYNGO1QCJCEQ) — DigiTimes
- [100] [DDR, LPDDR revenue growth outpaces HBM as DRAM market nears US$200 billion](https://www.digitimes.com/news/a20261106VL206/revenue-dram-ddr-hbm-market.html) — DigiTimes Asia
- [101] [Samsung, SK Hynix eye AI inference boom as South Korea's SSD exports soar 584%](https://www.digitimes.com/news/a20261106PD219/sk-hynix-samsung-ssd-exports-demand.html) — DigiTimes Asia
- [104] [SK Hynix AI arm buys US$377 million stake in Penguin Solutions from SK Telecom](https://www.digitimes.com/news/a20261106VL207/sk-hynix-solidigm-ai-investment.html) — DigiTimes Asia
- [105] [Stockpiled in Hong Kong: Beijing limits Nvidia H200 imports as domestic silicon push accelerates](https://www.digitimes.com/news/a20261106VL209/beijing-nvidia-silicon-market-shipments.html) — DigiTimes Asia
- [106] [AI需求強勁、T-Glass供不應求 日東紡再砸200億日圓擴產](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773798_X4382BZU81U3LU9LMWJWX) — DigiTimes
- [107] [資料中心延宕、成本增加 微軟對新雲端業者態度轉趨保守](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773810_ZCG7XVUJ25YMIILAOID96) — DigiTimes
- [108] [反對聲浪升高 OpenAI資料中心藍圖聚焦資訊透明與社區參與](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773813_QR79JARB08IML54LWBD1H) — DigiTimes
- [109] [JX金屬因應先進封裝與HBM 高純度硫酸銅擴產投資數十億日圓](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773806_ZE77W2S31A518O5Y6EJGK) — DigiTimes
- [111] [Meta faces political pushback over US data center expansion](https://www.digitimes.com/news/a20261106PD226/meta-expansion-data-infrastructure-investment.html) — DigiTimes Asia
- [112] [AI資料中心需求強勁 羅姆上修2026年度財測、淨利上看450億日圓](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773814_OU47D3L9271HM63AHJ3YO) — DigiTimes
- [113] [Samsung speeds P5 Fab 2 construction as memory chip shortage looks to last through 2028](https://www.digitimes.com/news/a20261105VL231/samsung-2028-2027-equipment-production.html) — DigiTimes Asia
- [114] [《路克相談室》EP67文字精華：蘋果大囤料簽長約鎖產能 供應鏈超額預訂風險上升 / 英特爾18A製程轉回Intel 3 產能調度捉襟見肘](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773829_0697N6DQ37SZP283MFAL3) — DigiTimes
- [116] [華虹宏力3Q26營收歷史新高 前3季獲利年增逾1.3倍](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773823_P0V9DB4V1M1Q5T4NP2R68) — DigiTimes
- [121] [Qualcomm validates HBC memory architecture, targets AI250 samples in 1H27](https://www.digitimes.com/news/a20261106PD216/qualcomm-hardware-ai-inference-technology-hbm4.html) — DigiTimes Asia
- [125] [Nvidia reportedly buys glass substrate samples from Korea's JNTC](https://www.digitimes.com/news/a20261106VL216/jntc-nvidia-glass-substrate-supplier-manufacturing.html) — DigiTimes Asia
- [127] [Moonshot AI reportedly seeking access to Nvidia GPUs through European neoclouds](https://www.digitimes.com/news/a20261106VL219/moonshot-nvidia-chips-blackwell-data.html) — DigiTimes Asia
- [128] [Commentary: US governors target AI data centers as Taiwan firms await Nvidia outlook](https://www.digitimes.com/news/a20261106PD241/usa-data-center-ai-outlook-2026.html) — DigiTimes Asia
- [131] [營收速報 - 京元電子(2449)10月營收44.26億元年增率高達29.47％](https://news.cnyes.com/news/id/6650439) — 鉅亨網
- [133] [聯發科侯上勇：CoWoS從有趣變頭痛 卡位封裝產能成當務之急](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773912_HB581UYA2MEQTT1OG8YE8) — DigiTimes
- [134] [US lawmakers request briefing with Nvidia's Jensen Huang on dealings with Megaspeed executive](https://www.digitimes.com/news/a20261106VL220/nvidia-jensen-huang-ceo-chips-government.html) — DigiTimes Asia
- [137] [群聯AI業務3Q26貢獻突破5成 追求三大財務指標延續成長](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773921_LYALCSK21H5HM52HHSJZG) — DigiTimes
- [138] [營收速報 - 欣興(3037)10月營收189.86億元年增率高達67.62％](https://news.cnyes.com/news/id/6651070) — 鉅亨網
- [139] [營收速報 - 力成(6239)10月營收87.27億元年增率高達25.2％](https://news.cnyes.com/news/id/6651084) — 鉅亨網
- [141] [營收速報 - 華邦電(2344)10月營收293.61億元年增率高達256.96％](https://news.cnyes.com/news/id/6651327) — 鉅亨網
- [142] [世界先進4Q26稼動率逾9成 方略：AI不可逆、過熱修正有助健康成長](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773931_WJY8B4UD4AQSMK0ZRIJHG) — DigiTimes
- [143] [世界先進新加坡12吋廠將成一大動能 中介層估佔VSMC營收5成](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773935_XT1L9LLR22ELLD6E5JXTU) — DigiTimes
- [146] [不蓋新廠改舊樓！傳輝達盯上阿波羅旗下Brightspeed舊電信大樓 打響算力突圍戰](https://news.cnyes.com/news/id/6650103) — 鉅亨網
- [147] [美股百年只有12家股王 輝達讓位蘋果 晨星：但寬護城河可撐20年超額獲利](https://news.cnyes.com/news/id/6649327) — 鉅亨網
- [148] [鉅亨速報 - Factset 最新調查：京元電子(2449-TW)目標價調降至330元，幅度約3.93%](https://news.cnyes.com/news/id/6649394) — 鉅亨網
- [150] [台積傳砸 450 億美元赴德州建兩座先進晶圓廠，目標 2029 年底前實現量產](https://technews.tw/2026/11/06/tsmc-45b-texas-2-advanced-fabs-mass-production-2029/) — TechNews
- [152] [政治變天掀AI股崩盤！富豪榜洗牌：輝達黃仁勳掉出前十、全球500大單日蒸發1850億美元](https://news.cnyes.com/news/id/6649346) — 鉅亨網
- [155] [彭博：美光科技因勞資糾紛未解，暫停桃園工廠計畫](https://technews.tw/2026/11/06/micron-pauses-work-on-4-5-billion-taiwan-plant-after-labor-spat/) — TechNews
- [161] [台股災難黑色星期五 護國神山亮跌停燈 一度多達500檔跌停](https://news.cnyes.com/news/id/6649661) — 鉅亨網
- [164] [SpaceX五年期CDS飆至284.3基點！民主黨大勝加劇馬斯克AI布局壓力](https://news.cnyes.com/news/id/6649464) — 鉅亨網
- [171] [選後行情變臉！那指盤中跌入修正區間 台積電ADR挫近7.6%](https://news.cnyes.com/news/id/6649126) — 鉅亨網
- [177] [1.8兆美元恐蒸發！AI基建怕卡關 那斯達克100遭血洗](https://news.cnyes.com/news/id/6649071) — 鉅亨網
- [178] [Commentary: Marvell's Lumentum deal holds a lesson for smartphone makers on supply chain integration](https://www.digitimes.com/news/a20261104PD254/marvell-smartphone-acquisition-supply-chain-market.html) — DigiTimes Asia
- [179] [Nscale's US$35 billion IPO faces fresh uncertainty after Microsoft rejects Texas AI capacity expansion](https://www.digitimes.com/news/a20261105PD234/ipo-infrastructure-capacity-microsoft-uk.html) — DigiTimes Asia
- [182] [美光勞資「信心危機」暫緩桃園無塵室工程 EUV設備訂單未變](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773760_NY86352B73QVLDLRF00IH) — DigiTimes
- [183] [【Amy & Dr. Chip】長鑫不夠好？ 阿里、騰訊、字節跳動搶簽南韓記憶體長約](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773275_OU3330SJ61II1T6KKFBF4) — DigiTimes
- [195] [Meta收購AI程式開發新創Conductor 布局多代理協作工具](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773731_4CV6LQSZ47BX0Z0NBWG1U) — DigiTimes
- [197] [蘋果逾一年來首度發債！擬籌70億美元 支應庫藏股、股利與資本支出](https://news.cnyes.com/news/id/6649030) — 鉅亨網
- [198] [Google擴大馬來西亞投資 未來2年加碼150億美元](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773664_EF15P1T57NG8I7357EBWZ) — DigiTimes
- [199] [DIGITIMES Insight: Foxconn extends AI strategy to data center system integration, targeting modular computing delivery with DSX POD](https://www.digitimes.com/news/a20261104PD241/foxconn-data-center-equipment-2026-cooling.html) — DigiTimes Asia
- [203] [AI引爆全球記憶體荒 晶創方案2027年新增先進記憶體計畫](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773670_7S6513U08QNK1KLSHKAWR) — DigiTimes
- [213] [DIGITIMES Today：晶創方案明年新增先進記憶體 | 美選舉變天 台廠29億美元投資受關注 | 台美組隊「混血無人艇」](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773754_RCE84YH2462LKG541XRBC) — DigiTimes
- [214] [民主黨大獲全勝後 參議員桑德斯呼籲「全美暫停」興建資料中心](https://news.cnyes.com/news/id/6649300) — 鉅亨網
- [215] [〈美股盤後〉AI股大逃殺！VIX狂飆逾60% 道瓊狂瀉1800點 費半血崩逾12% 台積電ADR下殺逾10%](https://news.cnyes.com/news/id/6648369) — 鉅亨網
- [216] [「馬斯克拋售潮」加劇！特斯拉、SpaceX兩日市值蒸發4560億美元](https://news.cnyes.com/news/id/6649269) — 鉅亨網
- [218] [AI 晶片趨向大面積化，英特爾強調 EMIB 封裝技術將迎接龐大商機挑戰台積電](https://technews.tw/2026/11/06/intel-emphasizes-that-emib-packaging-technology-will-usher-in-huge-business-opportunities/) — TechNews
- [223] [AMD teams up with FuriosaAI, MangoBoost to build Seoul AI cluster](https://www.digitimes.com/news/a20261105VL229/amd-south-korea-ai-chips-development-software.html) — DigiTimes Asia
- [224] [(News) MediaTek Reportedly Taps Intel Packaging Veteran After TSMC Hire, Advances Dual CoWoS–EMIB Strategy](https://www.trendforce.com/news/2026/11/06/news-mediatek-reportedly-taps-intel-packaging-veteran-after-tsmc-hire-advances-dual-cowos-emib-strategy/) — TrendForce
- [225] [美國45% AI資料中心擴建計畫恐遭凍結！德州政壇變天 13GW容量陷監管風暴](https://news.cnyes.com/news/id/6649299) — 鉅亨網
- [227] [Naver's Nvidia-backed AI factory faces crucial test after US$9 billion deal](https://www.digitimes.com/news/a20261105VL226/naver-infrastructure-gpu-launch-business.html) — DigiTimes Asia
- [228] [「科技七巨頭」市值合計失血1兆美元！周四科技股崩跌最驚人數據一次看](https://news.cnyes.com/news/id/6649319) — 鉅亨網
- [232] [AI doubts mount, but server supply chain still sees strong demand](https://www.digitimes.com/news/a20261105PD210/ai-server-asic-demand-supply-chain-nvidia-gpu.html) — DigiTimes Asia
- [233] [CXMT prepayments surge 16x with DRAM shortage lifting market share](https://www.digitimes.com/news/a20261105PD212/dram-cxmt-market-share-capacity-production.html) — DigiTimes Asia
- [234] [QuantumDiamonds targets HBM defects as it develops inline inspection tool](https://www.digitimes.com/news/a20261104VL226/hbm-startup-technology-wafer-inspection.html) — DigiTimes Asia
- [235] [Winbond approves US$2.2 billion fab expansion, seeks long-term deals with 10 customers](https://www.digitimes.com/news/a20261104PD242/winbond-fab-expansion-equipment-wafer.html) — DigiTimes Asia
- [236] [SK Hynix leads HBM4 yield at 60%, expands DRAM supply](https://www.digitimes.com/news/a20261105PD211/sk-hynix-hbm4-dram-hbm-capacity.html) — DigiTimes Asia
- [237] [Samsung reportedly plans 2nm fab to boost HBM base-die output](https://www.digitimes.com/news/a20261105VL216/samsung-fab-hbm-2nm-production.html) — DigiTimes Asia
- [238] [Arm 3QFY26財測僅小勝預期 AI資料中心展望仍待驗證](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773644_LSB5TKLY5WK1FA3C8IGXH) — DigiTimes
- [240] [US pressure on overseas AI compute squeezes Chinese tenants and Southeast Asian data centers as Beijing pushes domestic chips](https://www.digitimes.com/news/a20261105VL209/ai-chip-data-center-usa-beijing-nvidia-tencent.html) — DigiTimes Asia
- [241] [Meta首發歐元債 認購需求創紀錄達發行額近6倍](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773645_CRO7RVDG3W7DRA6FSPCWR) — DigiTimes
- [242] [Naver Cloud ramps up use of AMD EPYC, citing high Intel CPU costs](https://www.digitimes.com/news/a20261105PD209/cloud-naver-amd-intel-cpu.html) — DigiTimes Asia
- [243] [South Korea's Moreh claims AMD MI355X delivers over twice Nvidia B200's inference throughput](https://www.digitimes.com/news/a20261105VL217/moreh-amd-nvidia-software-government.html) — DigiTimes Asia
- [244] [RTX Pro 5500到貨率僅1% 中國AI大廠面臨嚴峻NVIDIA晶片荒](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773639_PVV5QA1Q4ET6BM8BI9H3D) — DigiTimes
- [246] [Analysis: Qualcomm's AI server CPU ambitions gain urgency as smartphone slump threatens its core business](https://www.digitimes.com/news/a20261105VL211/qualcomm-business-smartphone-cpu-revenue.html) — DigiTimes Asia
- [250] [格羅方德3Q26營收年增13% AI與資料中心改寫收入結構](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000773640_A1G7NCBG3G0KAF1PSYL3A) — DigiTimes
