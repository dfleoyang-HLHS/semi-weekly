#!/usr/bin/env python3
"""
fetch_youtube.py
整理財經節目 YouTube 頻道的影片,產生「影音觀點」頁面的資料。

只使用 YouTube 官方管道取得的公開資訊 (不下載影片、不抓字幕):
  - 有 YOUTUBE_API_KEY:YouTube Data API v3,可回溯指定天數 (預設 14 天)
  - 沒有金鑰:頻道官方 RSS (僅最近 15 支影片,約 2~3 天)

整理方式 (不經 AI 改寫,內容皆來自創作者自己的標題與說明欄):
  - 依節目日期把「完整版、分段 (part1~3)、精華短片」歸為同一集
  - 節目章節 (說明欄時間軸)、主題標籤、來賓
  - 提到的公司:比對證交所 / 櫃買中心上市櫃公司名稱與常見暱稱 (如 發哥 → 聯發科)

設定:data/youtube_channels.json      輸出:data/youtube.json (影片累積保存)
用法:python scripts/fetch_youtube.py [--days 14]
"""

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
CHANNELS = DATA / "youtube_channels.json"
OUT = DATA / "youtube.json"
COMPANY_NAMES = DATA / "tw_company_names.json"
TZ = timezone(timedelta(hours=8))
API = "https://www.googleapis.com/youtube/v3"

# ── 公司辨識 ──────────────────────────────────────────────
# 兩字簡稱常與一般詞彙重疊 (如 統一、幸福),只採用下列科技 / AI 供應鏈相關公司
TW_SHORT_OK = set("""聯電 鴻海 廣達 緯創 和碩 華碩 宏碁 友達 群創 彩晶 凌巨 欣興 南電 景碩 力成 技嘉 微星 仁寶 光寶 國巨
華通 健鼎 奇鋐 雙鴻 精測 穩懋 宏捷 聯詠 瑞昱 創意 信驊 祥碩 譜瑞 旺宏 威剛 群聯 十銓 創見 家登 弘塑 辛耘 萬潤 均豪 志聖
牧德 尖點 聯茂 台燿 嘉澤 川湖 勤誠 營邦 貿聯 信邦 光聖 上詮 聯亞 眾達 前鼎 合晶 漢磊 嘉晶 鈺創 智原 力旺 神盾 義隆 原相
敦泰 天鈺 致新 茂達 立積 頎邦 南茂 矽格 欣銓 菱生 超豐 晶技 台郡 定穎 金居 銘異 緯穎 宇隆 致茂 京元 健策 宏達電""".split())
# 暱稱 / 常用全名 → 官方簡稱
TW_ALIAS = {"發哥": "聯發科", "台積": "台積電", "日月光": "日月光投控", "世界先進": "世界", "京元電": "京元電子",
            "華邦": "華邦電", "南亞科技": "南亞科", "世芯": "世芯-KY", "矽力": "矽力*-KY",
            "臻鼎": "臻鼎-KY", "緯穎科技": "緯穎", "華星光通": "華星光"}
US_ALIAS = {
    "NVDA": ["輝達", "NVIDIA", "Nvidia"], "AMD": ["超微", "AMD"], "INTC": ["英特爾", "Intel"],
    "MU": ["美光", "Micron"], "AVGO": ["博通", "Broadcom"], "AAPL": ["蘋果", "Apple"],
    "GOOGL": ["谷歌", "Google", "Alphabet"], "MSFT": ["微軟", "Microsoft"], "AMZN": ["亞馬遜", "Amazon"],
    "TSLA": ["特斯拉", "Tesla"], "META": ["Meta", "臉書"], "MRVL": ["邁威爾", "Marvell"],
    "QCOM": ["高通", "Qualcomm"], "ORCL": ["甲骨文", "Oracle"], "DELL": ["戴爾", "Dell"],
    "SMCI": ["美超微", "Supermicro"], "ARM": ["安謀", "Arm"], "TSM": ["台積電ADR"],
}
US_NAME = {"NVDA": "輝達", "AMD": "超微", "INTC": "英特爾", "MU": "美光", "AVGO": "博通", "AAPL": "蘋果",
           "GOOGL": "谷歌", "MSFT": "微軟", "AMZN": "亞馬遜", "TSLA": "特斯拉", "META": "Meta", "MRVL": "邁威爾",
           "QCOM": "高通", "ORCL": "甲骨文", "DELL": "戴爾", "SMCI": "美超微", "ARM": "安謀", "TSM": "台積電 ADR"}


def load_tw_names():
    """上市櫃公司簡稱 → (代號, 市場)。由 fetch_tw_prices 的官方資料建立並快取。"""
    if COMPANY_NAMES.exists():
        return json.loads(COMPANY_NAMES.read_text(encoding="utf-8"))
    sys.path.insert(0, str(Path(__file__).parent))
    from fetch_tw_prices import get_json, TWSE_DAILY, TPEX_DAILY
    names = {}
    for x in get_json(TWSE_DAILY):
        if re.fullmatch(r"\d{4}", x.get("Code", "")):
            names[x["Name"].strip()] = [x["Code"], "上市"]
    for x in get_json(TPEX_DAILY):
        if re.fullmatch(r"\d{4}", x.get("SecuritiesCompanyCode", "")):
            names[x["CompanyName"].strip()] = [x["SecuritiesCompanyCode"], "上櫃"]
    COMPANY_NAMES.write_text(json.dumps(names, ensure_ascii=False, indent=0), encoding="utf-8")
    return names


# 官方簡稱不易辨識時的顯示名稱
TW_DISPLAY = {"5347": "世界先進"}


def build_matchers(tw_names):
    matchers = []  # (比對文字, 顯示名稱, 代號, 市場)
    for name, (code, market) in tw_names.items():
        base = name.replace("-KY", "").replace("*", "")
        if len(base) >= 3 or base in TW_SHORT_OK:
            matchers.append((base, TW_DISPLAY.get(code, name), code, market))
    for alias, official in TW_ALIAS.items():
        if official in tw_names:
            code, market = tw_names[official]
            matchers.append((alias, TW_DISPLAY.get(code, official), code, market))
    for code, aliases in US_ALIAS.items():
        for a in aliases:
            matchers.append((a, US_NAME[code], code, "美股"))
    # 長的名稱先比對,避免「台積電ADR」被當成「台積電」
    return sorted(matchers, key=lambda m: -len(m[0]))


def find_companies(text, matchers):
    found, taken = {}, [False] * len(text)
    for key, name, code, market in matchers:
        ascii_key = key.isascii()
        for m in re.finditer(re.escape(key), text, re.IGNORECASE if ascii_key else 0):
            s, e = m.span()
            if ascii_key and ((s > 0 and text[s - 1].isalnum()) or (e < len(text) and text[e].isalnum())):
                continue
            if any(taken[s:e]):
                continue
            for i in range(s, e):
                taken[i] = True
            found[code] = {"name": name, "code": code, "market": market}
    return list(found.values())


# ── 取得影片 ──────────────────────────────────────────────
def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (semi-weekly)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def videos_from_api(channel_id, key, since):
    ch = get_json(f"{API}/channels?{urllib.parse.urlencode({'part': 'contentDetails', 'id': channel_id, 'key': key})}")
    uploads = ch["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    out, token = [], None
    while True:
        q = {"part": "snippet", "playlistId": uploads, "maxResults": 50, "key": key}
        if token:
            q["pageToken"] = token
        data = get_json(f"{API}/playlistItems?{urllib.parse.urlencode(q)}")
        for it in data.get("items", []):
            sn = it["snippet"]
            published = sn.get("publishedAt", "")
            if published and published < since:
                return out
            vid = sn.get("resourceId", {}).get("videoId")
            if vid and sn.get("title") not in ("Private video", "Deleted video"):
                out.append({"id": vid, "title": sn["title"], "published": published, "description": sn.get("description", "")})
        token = data.get("nextPageToken")
        if not token:
            return out


def videos_from_rss(channel_id):
    import feedparser
    f = feedparser.parse(f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")
    return [{"id": e.get("yt_videoid") or e.link.split("v=")[-1], "title": e.title,
             "published": e.get("published", ""), "description": e.get("summary", "")} for e in f.entries]


# ── 整理 ─────────────────────────────────────────────────
def to_local_date(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(TZ).date().isoformat()


def parse_video(v, cfg, matchers):
    title, desc = v["title"].strip(), v.get("description", "")
    published = to_local_date(v["published"])
    m = re.search(r"(\d{4})\.(\d{2})\.(\d{2})", title)
    show_date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else published
    part = re.search(r"part\s*(\d)", title, re.IGNORECASE)
    if cfg.get("podcast_mark") and cfg["podcast_mark"] in title:
        kind = "podcast"
    elif part:
        kind = "part"
    elif cfg.get("episode_mark") and title.startswith(cfg["episode_mark"]):
        kind = "full"
    else:
        kind = "clip"
    guests = []
    if "｜" in title:  # 「…｜李兆華、朱家泓 2026.09.30 part1」:先去掉日期與分段,再依頓號拆開
        tail = title.split("｜")[-1].split("【")[0]
        tail = re.sub(r"\s*\d{4}\.\d{2}\.\d{2}.*$", "", tail)
        guests = [g.strip() for g in re.split(r"[、,，]", tail) if g.strip()]
    for f in re.findall(r"feat\.\s*([^\s#]+)", title, re.IGNORECASE):
        guests.append(f)
    chapters = [{"time": t, "topic": c.strip()} for t, c in
                re.findall(r"^\(?(\d{1,2}:\d{2}(?::\d{2})?)\)?\s+(.+)$", desc, re.MULTILINE)]
    hashtags = [h for h in re.findall(r"#([^\s#]+)", desc + " " + title)
                if h not in cfg.get("ignore_tags", []) and not re.fullmatch(r"\d[\dA-Z]*", h)]  # 去掉 ETF 代號 (如 00416A)
    clean_title = re.sub(r"\s*#\S+", "", title).replace("👑", "").strip()
    text = " ".join([title, " ".join(c["topic"] for c in chapters), " ".join(hashtags)])
    return {
        "id": v["id"], "channel": cfg["name"], "kind": kind, "title": clean_title,
        "published": published, "show_date": show_date,
        "guests": [g for g in dict.fromkeys(guests) if g],
        "chapters": chapters, "hashtags": list(dict.fromkeys(hashtags)),
        "companies": find_companies(text, matchers),
        "part": int(part.group(1)) if part else None,
    }


def build_episodes(videos, cfg):
    """完整版 / 分段 / 精華短片 依節目日期與來賓歸為同一集"""
    eps = {}
    for v in sorted(videos, key=lambda x: x["published"]):
        if v["channel"] != cfg["name"] or v["kind"] not in ("full", "part"):
            continue
        ep = eps.setdefault(v["show_date"], {"channel": cfg["name"], "date": v["show_date"], "full": None,
                                             "parts": [], "clips": [], "guests": []})
        if v["kind"] == "full":
            ep["full"] = v
        else:
            ep["parts"].append(v)
        ep["guests"] = list(dict.fromkeys(ep["guests"] + v["guests"]))
    # 精華短片:來賓 (feat. 標示,或來賓姓名出現在標題中) 屬於某集,且發布日為該集當天或之後 3 天內
    orphans = []
    for v in videos:
        if v["channel"] != cfg["name"] or v["kind"] != "clip":
            continue
        def match(e):
            names = set(e["guests"]) - {cfg.get("host")}
            return bool(set(v["guests"]) & names) or any(n and n in v["title"] for n in names)
        cands = [e for d, e in eps.items() if match(e)
                 and 0 <= (datetime.fromisoformat(v["published"]) - datetime.fromisoformat(d)).days <= 3]
        if cands:
            max(cands, key=lambda e: e["date"])["clips"].append(v)
        else:
            orphans.append(v)  # 無法確定屬於哪一集 (如只用暱稱),另列於「其他精華短片」
    out = []
    for ep in eps.values():
        ep["parts"].sort(key=lambda p: p["part"] or 0)
        allv = ([ep["full"]] if ep["full"] else []) + ep["parts"] + ep["clips"]
        comp = {}
        for v in allv:
            for c in v["companies"]:
                comp.setdefault(c["code"], {**c, "count": 0})["count"] += 1
        ep["companies"] = sorted(comp.values(), key=lambda c: -c["count"])
        ep["hashtags"] = list(dict.fromkeys(h for v in allv for h in v["hashtags"]))
        ep["title"] = (ep["full"] or ep["parts"][0])["title"]
        host = cfg.get("host")
        ep["guests"] = [g for g in ep["guests"] if g != host]
        ep["host"] = host
        out.append(ep)
    others = [v for v in videos if v["channel"] == cfg["name"] and v["kind"] == "podcast"] + orphans
    return sorted(out, key=lambda e: e["date"], reverse=True), sorted(others, key=lambda v: v["published"], reverse=True)


def main():
    days = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 14
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    channels = json.loads(CHANNELS.read_text(encoding="utf-8"))["channels"]
    key = os.environ.get("YOUTUBE_API_KEY")
    matchers = build_matchers(load_tw_names())

    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    store = {v["id"]: v for v in old.get("videos", [])}
    for cfg in channels:
        raw = videos_from_api(cfg["channel_id"], key, since) if key else videos_from_rss(cfg["channel_id"])
        for v in raw:
            store[v["id"]] = parse_video(v, cfg, matchers)
        print(f"  {cfg['name']}: 取得 {len(raw)} 支影片 ({'Data API' if key else 'RSS'})")

    keep_from = (datetime.now(TZ).date() - timedelta(days=days)).isoformat()
    videos = [v for v in store.values() if v["published"] >= keep_from]
    episodes, extras = [], []
    for cfg in channels:
        e, x = build_episodes(videos, cfg)
        episodes += e
        extras += x
    OUT.write_text(json.dumps({
        "updated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "days": days, "source": "YouTube Data API" if key else "YouTube 頻道 RSS",
        "channels": channels, "episodes": episodes, "extras": extras, "videos": videos,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"✅ 影音觀點:{len(episodes)} 集、{len(videos)} 支影片 (近 {days} 天)")


if __name__ == "__main__":
    main()
