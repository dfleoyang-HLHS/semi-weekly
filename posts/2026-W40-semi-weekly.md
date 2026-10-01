---
title: "半導體 + AI 供應鏈週報 (2026-W40)"
date: 2026-10-01
week: "2026-W40"
category: "週報"
regions: ["美國", "台灣", "日本", "韓國", "中國大陸", "歐洲"]
companies:
  - Micron
  - NVIDIA
  - AMD
  - Broadcom
  - Google
  - Intel
  - TSMC
  - ASE
  - Unimicron
  - MediaTek
  - SK Hynix
  - Samsung
  - JCET
  - TFME
  - Huawei
  - HPE
  - AWS
  - Netlist
tags: ["HBM", "記憶體超級循環", "ASIC", "先進封裝", "玻璃基板", "ABF 載板", "AI 代理", "專利訴訟"]
summary: "美光 FQ4 營收 542 億美元、毛利率 86.8% 雙創新高,客戶已提前鎖定 2027 年供給;DIGITIMES 預估 2027 年雲端 AI ASIC 出貨將首度超越 GPU。AMD 以 82 億美元收購 World Labs,Netlist 對美光、NVIDIA、Broadcom、Google 提起 HBM 專利訴訟。"
cover_image: ""
---

## 本週重點

美光 FQ4 (截至 9/3) 營收 542 億美元、季增 31%,GAAP 毛利率衝上 86.8%,成長主要來自漲價而非出貨量,客戶已預付資金鎖定 2027 年供給 [3][14],記憶體缺貨恐延續數年 [44]。DIGITIMES 預估 2027 年雲端 AI ASIC 總出貨將首度超越 GPU,市場進入「NVIDIA 與 Google 雙強」格局,ABF 載板瓶頸也隨之轉移 [10]。先進封裝產能競賽持續:欣興砸 100 億元在湖口購地擴產高階載板 [13]、日月光買下新加坡廠擴充 AI 測試 [46],陸系 OSAT 在雲端 AI 加速器封裝市佔預估由 3.9% 跳升至 13% [18]。另外,Netlist 對美光及下游 NVIDIA、Broadcom、Google 提起 HBM 專利訴訟,是 HBM 供應鏈新的法律變數 [48]。

---

## 一、產業全貌

**主軸一:記憶體由「量」轉「價」的超級循環。** 美光的財報說明本輪記憶體成長主要靠定價權:營收季增 31%,毛利率 86.8% [3]。三星也坦言,沒料到 AI 會大幅帶動 HBM 以外的記憶體需求;產能集中到 HBM 後,一般 DRAM 每片晶圓的獲利反而更高 [26]。群聯執行長潘健成則認為供需缺口可能要很多年才能補上 [44]。副作用開始浮現:韓媒指三星 MX/NW 事業部 3Q26 可能因記憶體漲價虧損逾 1 兆韓元 [36]。

**主軸二:ASIC 崛起、多家「組隊」設計。** DIGITIMES 預估 2027 年 Google、Amazon 與華為帶動 ASIC 出貨超越 GPU [10];CSP 擴大 ASIC 合作夥伴,單一 ASIC 整合多家技術漸成主流,一家包辦的時代或將結束 [41]。聯發科 Google TPU 訂單穩中向上,供應鏈產能爭奪進入短兵相接 [17];AWS Trainium 3 則因長短料與系統組裝問題出貨暫時卡關 [38]。

---

## 二、美國 (USA)

### NVIDIA
- 9/28 發布開放式 AI 代理安全平台,結合 OpenShell 軟體與基於 BlueField-4 的 Sentry 硬體監控器,主張用 DPU 硬體控管 AI 代理 [31][33];OpenAI 未列入合作夥伴名單 [11]。
- 黃仁勳獲頒 Van Fleet 獎,三星李在鎔、SK 崔泰源到場,NVIDIA 與韓國的合作已從記憶體供應延伸到 AI 製造 [5]。
- 9 月初宣布以約 129 億美元收購 Hugging Face [42]。

### AMD
- 以約 82 億美元全股票交易收購 World Labs,李飛飛出任執行副總裁兼首席科學家,切入具身智慧 [34]。
- 採台積電 2 奈米的 Zen 6 Venice EPYC 處理器,2027 年產能已售罄,反映代理式 AI 帶動的 CPU 需求 [12]。
- HPE 拿下 Vultr 12 億美元 AMD Helios AI 機櫃訂單 [1];ROCm 10.0 已可在 SiFive RISC-V 資料中心伺服器上執行 [43]。

### Micron / Broadcom / Google / Intel
- **Micron**:FQ4 營收 542 億美元、毛利率 86.8%,單季及全年皆創紀錄 [3][14];遭 Netlist 提起 HBM 專利訴訟 [48]。
- **Broadcom**:於 TSMC OIP 論壇分享 ASIC 與生態系觀點 [16];與 NVIDIA、Google 同列 Netlist 訴訟被告 [48]。
- **Google**:10/1 啟動 Suncatcher 計畫,首度把 TPU 送上近地軌道測試 [32]。
- **Intel**:執行長陳立武表示 Intel 與台積電是夥伴而非對手 [7]。
- **其他**:Synopsys 與 OpenAI 共同開發 GPT-Synopsys,雙方分潤 [2];AWS Trainium 3 出貨暫時卡關,AWS 參與金像電私募以確保料源 [38]。

---

## 三、台灣 (Taiwan)

### 台積電 TSMC (2330.TW)
- 台積電於 SEMICON Taiwan 揭示 AI 算力擴展由單晶片微縮走向系統級異質整合 [35];OIP 論壇強調 3D 多晶粒的跨晶粒複雜度已成為設計問題 [56]。
- 下一代玻璃基板規格浮現:康寧、AGC、NEG、肖特四大玻璃廠不約而同選擇 510×515mm 尺寸 [30];面板廠也藉玻璃基板跨入先進封裝 [53]。
- 卓榮泰在立法院表示支持台積電赴美,但核心研發留在台灣 [45]。

### 日月光投控 ASE (3711.TW)
- 新加坡子公司以約 6,844 萬美元 (約新台幣 21.52 億元) 向 Lumileds 購買義順工業區廠房,支援未來產能擴充 [46]。
- 7 月以約 56.72 億元向乖乖取得中壢工業區廠房,乖乖工會發起罷工投票並至中壢廠抗議 [15]。
- 日月光擴產帶動檢測設備廠牧德半導體業務進入「產品認證、擴大接單」階段 [29]。

### 京元電 KYEC (2449.TW) / 力成 PTI (6239.TW)
- 本週無重大進展。

### 基板與材料 (欣興、南電、景碩)
- **欣興**:取得新竹湖口不動產,總金額約新台幣 100 億元,因應高階載板擴產需求 [13]。
- **牧德**:2027 年成長動能以半導體與載板最強,部分載板大客戶需求能見度達 3 年 [27]。

### IC 設計與其他
- **聯發科**:Google TPU 訂單穩中向上 [17]。
- **南科**:1H26 營收 1.77 兆元、年增 28.57%,AI 為主要動能 [6]。

---

## 四、日本 (Japan)

### Ibiden (4062.T) / Shinko / Resonac / Ajinomoto
- 本週無直接公司消息;DIGITIMES 指 2027 年 ASIC 放量將使 ABF 載板瓶頸轉移,值得追蹤日系載板廠接單變化 [10]。

### 設備廠 (TEL, SCREEN, Disco)
- 本週無重大進展。日系玻璃廠 AGC、NEG 已將核心玻璃基板對準 510×515mm 規格 [30]。

---

## 五、韓國 (South Korea)

### SK Hynix (000660.KS)
- 睽違 4 年 (2023 年中斷) 再將 DDR4/DDR5 封裝委外給韓國封測廠 Winpac,擴大外部覆晶封裝比重 [25][52]。

### Samsung Electronics (005930.KS)
- HBM4 量產帶動 4 奈米邏輯產線 (base die) 需求,為晶圓代工帶來助力,同時持續推進 2 奈米 [4]。
- 三星 6 家關係企業共同投資 Helix,砸 10 億美元擴大 AI [47];Samsung AI Forum 2026 定調代理式 AI 為轉型核心 [39]。
- 三星電機 2026 年第 5 份 AI 伺服器 MLCC/電感長約入袋 (約 2,900 億韓元),全年 LTA 累計 3.6 兆韓元 [24];三星 SDI 推出資料中心用圓柱型 LFP 電池 [54]。
- 韓國 8 吋代工 DB HiTek 今年兩度漲價,幅度約 5~30% [22]。

---

## 六、中國大陸 (China)

### 長電科技 JCET (600584.SS) / 通富微電 TFME
- 華為、寒武紀、阿里巴巴的 ASIC 加速器逐步放量,交由長電、通富微電、盛合晶微封裝;DIGITIMES 預估中國 OSAT 在雲端 AI 加速器封裝市佔將由 2025 年的 3.9% 升至 2026 年的 13% [18]。

### 中芯國際 SMIC / 華為體系
- 華為為 2027 年 ASIC 出貨超越 GPU 的三大推手之一 [10];手機已重回中國市場銷售第一 [19]。
- 中國資料中心已交付容量超過 24GW,為全球第二大市場 [40];字節跳動約占其中五分之一,是最大的租用算力客戶 [23][55]。

---

## 七、歐洲 (Europe)

### ASML / BESI / AT&S / Infineon / STMicro
- 本週無重大進展。德國肖特 (Schott) 同樣將玻璃基板鎖定 510×515mm 規格 [30]。

---

## 八、本週財報重點

| 公司 | 期別 | 營收 | YoY | 重點 |
|------|------|------|------|------|
| Micron | FY26 Q4 (截至 2026/9/3) | 542 億美元 (QoQ +31%) | 待確認 | GAAP 毛利率 86.8%;單季及全年皆創紀錄;客戶預付鎖定 2027 年供給 [3][14] |

---

## 九、風險與下週觀察點

1. **Netlist HBM 專利訴訟**:追蹤是否申請禁制令,以及對美光 HBM 出貨與 NVIDIA/Broadcom/Google 採購的影響 [48]。
2. **AWS Trainium 3 出貨**:長短料與系統組裝問題何時解除,金像電等供應鏈出貨能否在 4Q26 回升 [38]。
3. **記憶體漲價外溢**:三星 MX/NW 3Q26 實際虧損數字 (10 月下旬法說),觀察終端品牌是否開始砍單 [36]。
4. **日月光中壢擴產**:乖乖工會罷工投票結果與廠房交接時程 [15]。
5. **玻璃基板規格**:台積電是否正式採用 510×515mm 尺寸,以及對 ABF 載板廠的長期影響 [30][10]。

---

## 資料來源

- [1] [HPE拿下Vultr機櫃大單 網通財測同步上修](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000770113_TQO23OBJ00P90W4G2PNSF) — DigiTimes
- [2] [Synopsys and OpenAI to share revenue from AI model built to run chip design tools](https://www.digitimes.com/news/a20261001VL202/synopsys-design-openai-eda-2026.html) — DigiTimes Asia
- [3] [Micron's record quarter rests on pricing power as customers lock in 2027 supply](https://www.digitimes.com/news/a20261001VL200/micron-2027-revenue-dram-price.html) — DigiTimes Asia
- [4] [Samsung Foundry gets boost from HBM4 as 2nm push continues](https://www.digitimes.com/news/a20260930VL221/samsung-foundry-hbm4-2nm-business-demand.html) — DigiTimes Asia
- [5] [Jensen Huang wins Van Fleet Award as Nvidia, South Korea trio reunites](https://www.digitimes.com/news/a20260930PD249/nvidia-jensen-huang-ceo-samsung-sk-group-partnership.html) — DigiTimes Asia
- [6] [AI boom drives Southern Taiwan Science Park revenue past NT$1.7 trillion in 1H26](https://www.digitimes.com/news/a20260929PD252/southern-taiwan-science-park-revenue-2026-taiwan-demand.html) — DigiTimes Asia
- [7] [Lip-Bu Tan calls TSMC a partner rather than a rival](https://www.digitimes.com/news/a20260930PD246/intel-lip-bu-tan-tsmc-partnership.html) — DigiTimes Asia
- [10] [ASIC shipments top GPUs in 2027 as ABF substrate bottlenecks shift](https://www.digitimes.com/news/a20260930PD237/asic-abf-substrate-cloud-ai-gpu-2027.html) — DigiTimes Asia
- [11] [Nvidia pushes full-stack AI agent security as OpenAI sits out partner roster](https://www.digitimes.com/news/a20260930PD204/nvidia-security-openai-software-technology.html) — DigiTimes Asia
- [12] [台積電 2 奈米製程加持,AMD Zen 6 架構 Venice EPYC 處理器 2027 年產能售罄](https://finance.technews.tw/2026/10/01/amds-zen-6-architecture-venice-epyc-processors-have-sold-out-for-2027/) — TechNews
- [13] [欣興砸百億湖口買地,因應持續擴產高階載板需求](https://finance.technews.tw/2026/10/01/xinxing-spends-billions-to-buy-land-in-hukou/) — TechNews
- [14] [美光 2026 年第四季毛利率衝上 86.8%,單季及全年財報均創歷史記錄](https://finance.technews.tw/2026/10/01/microns-gross-margin-surged-to-86-8-in-the-fourth-quarter-of-2026/) — TechNews
- [15] [DIGITIMES Today;華為手機大復活 | AWS Trainium 3出貨暫卡關](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000770085_0V0LU7IN9F7H3F4M8YQDH) — DigiTimes
- [16] [TSMC OIP Ecosystem Forum 2026: Broadcom's View of ASICs and Ecosystems](https://semiwiki.com/semiconductor-manufacturers/tsmc/374145-tsmc-oip-ecosystem-forum-2026-broadcoms-view-of-asics-and-ecosystems/) — SemiWiki
- [17] [聯發科TPU訂單穩中向上 搶供應鏈產能進入「短兵相接」](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000770032_SRCLMD8L460P8B1QHFB8N) — DigiTimes
- [18] [中系業者ASIC加速器放量 中國OSAT封裝市佔2026年衝13%](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000770045_YRX12JE43IFCS869W5E9T) — DigiTimes
- [19] [華為智慧手錶手環全球市佔逾2成 藍牙耳機挑戰前三強](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000770035_SLXLR3074LH42Q4FL4DBX) — DigiTimes
- [22] [DB HiTek 8吋晶圓代工最高漲3成](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000769900_CYX8LVMH1LAGYDLGOALGV) — DigiTimes
- [23] [字節跳動吃下中國20%資料中心容量 AI基建軍備戰升溫](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000769873_MQ39XXQN6ZT9W04RLK0UC) — DigiTimes
- [24] [三星電機2026年第5份LTA入袋 MLCC長約客戶已逾10家](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000770019_QS8LHRSF2QP1LO8U38MNU) — DigiTimes
- [25] [曾因三星訂單中斷合作 南韓Winpac睽違4年重拿SK海力士訂單](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000769977_G3WL78PC6DJMGL8KWQMYJ) — DigiTimes
- [26] [AI大幅帶動HBM以外的記憶體需求 三星也坦言始料未及](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000769924_GMLLO6B0131D3C57MEHTV) — DigiTimes
- [27] [牧德「雙軌四線」步入成長初期 半導體、載板能見度拉長達3年](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000770086_42TLN2KC97D2005LIFO5O) — DigiTimes
- [29] [日月光入股再擴產替牧德開門 半導體設備搶封測放量商機](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000770091_61T1P2U78GAZL32D7VNLW) — DigiTimes
- [30] [四大玻璃廠齊攻同一尺寸 台積電下一代玻璃基板規格呼之欲出?](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000770037_ON8LJ4TL42Z6X66GKNK2L) — DigiTimes
- [31] [黃仁勳出手、拋DPU硬體阻AI代理失控 五大議題發酵](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000769958_I58LF38N4C5YY49SC4SJ3) — DigiTimes
- [32] [Google自研TPU首度上太空 啟動Suncatcher測試](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000769793_LUC8F1KX8JGDXO4RGL1YH) — DigiTimes
- [33] [NVIDIA結合DPU與Vera CPU 鼓勵AI基建「全面標準化」](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000769957_5ZQLK0DQ4A100184W7CSB) — DigiTimes
- [34] [評析:超微挑戰NVIDIA具身智慧 黃仁勳眼看蘇姿丰將李飛飛團隊收入麾下](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000769965_7Z58HPEB7U5N7T4VZXOF1) — DigiTimes
- [35] [Research Insight:台積電揭AI算力擴展新路徑 異質整合走向系統級擴展](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000769777_UDE8F7MW6AQ1SH8NVT5TB) — DigiTimes
- [36] [折疊新機熱賣也救不了? 三星MX/NW 3Q26恐虧損逾兆韓元](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000769915_FV0L2PTZ0VCU956BWK6PF) — DigiTimes
- [38] [AWS Trainium 3出貨暫卡關 供應鏈:撥雲終見日](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000770047_NMZLW9CB5QL88D6PUQ4X2) — DigiTimes
- [39] [三星AI論壇啟動工作革命 定調「代理式AI」為轉型核心](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000770031_Q3O1S3N22K16RT2GNHRQR) — DigiTimes
- [40] [中國資料中心衝全球第二 四大網路巨擘資本支出猛增](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000769964_SAOL5DSH52UYIN5H5SKSA) — DigiTimes
- [41] [CSP改採ASIC多家技術「組隊」新趨勢 一家獨拿或成絕響](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000770024_AETLQ4IU3X42WV36LF50A) — DigiTimes
- [42] [科技巨擘買下AI預言?晶片商擬從水晶球提早看需求變化](https://www.digitimes.com.tw/tech/dt/n/shwnws.asp?id=0000769966_BD9LU3AZ5M8NTI7GMEK59) — DigiTimes
- [43] [SiFive and AMD Bring ROCm to RISC-V Datacenter Servers](https://semiwiki.com/ip/sifive/374137-sifive-and-amd-bring-rocm-to-risc-v-datacenter-servers-and-why-it-matters/) — SemiWiki
- [44] ['I tell myself every day it'll ease': Phison CEO sees years of memory shortage](https://www.digitimes.com/news/a20260930PD248/phison-ceo-demand-dram-acer.html) — DigiTimes Asia
- [45] [Taiwan backs TSMC's US push but insists core R&D stays home](https://www.digitimes.com/news/a20260930PD240/taiwan-tsmc-manufacturing-development-government.html) — DigiTimes Asia
- [46] [ASE Technology buys Singapore factory for AI chip testing expansion](https://www.digitimes.com/news/a20260930PD244/ase-testing-expansion-manufacturing-packaging.html) — DigiTimes Asia
- [47] [三星 6 家企業聯手投資 Helix,砸 10 億美元擴大 AI](https://technews.tw/2026/09/30/samsung-6-companies-invest-1-billion-helix-ai-expansion/) — TechNews
- [48] [Netlist challenges Micron, Nvidia, Broadcom, Google over alleged HBM patent use](https://www.digitimes.com/news/a20260930VL219/micron-patent-nvidia-broadcom-hbm.html) — DigiTimes Asia
- [52] [SK Hynix resumes DDR4, DDR5 packaging orders with Winpac](https://www.digitimes.com/news/a20260930VL218/sk-hynix-packaging-ddr5-ddr4-outsourcing.html) — DigiTimes Asia
- [53] [AI boom draws display makers into semiconductors with glass core substrates and Micro LED](https://www.digitimes.com/news/a20260930PD221/display-semiconductors-packaging-growth-technology.html) — DigiTimes Asia
- [54] [Samsung SDI targets AI data centers with cylindrical LFP batteries](https://www.digitimes.com/news/a20260930PD228/samsung-sdi-data-data-center-fire-lfp-battery.html) — DigiTimes Asia
- [55] [ByteDance makes up a fifth of China's AI data center capacity](https://www.digitimes.com/news/a20260930VL216/bytedance-data-center-capacity-infrastructure.html) — DigiTimes Asia
- [56] [Why Advanced Chip Packaging Is Becoming a Design Problem](https://semiwiki.com/semiconductor-manufacturers/tsmc/374150-why-advanced-chip-packaging-is-becoming-a-design-problem/) — SemiWiki
