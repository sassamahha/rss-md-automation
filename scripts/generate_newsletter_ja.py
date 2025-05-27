#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch latest StudyRiver & Sasakiya feeds via WP-REST and emit a Markdown file
into 5.NewsLetter/  (run inside repo root)
"""
import json, pathlib, requests, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "05.NewsLetter" / "ja"
OUTPUT_DIR.mkdir(exist_ok=True)

TODAY = datetime.date.today()            # 例: 2025-06-02
fname = f"{TODAY.isoformat()}-newsletter.md"
out_path = OUTPUT_DIR / fname

# ---------- 取得対象定義 ----------
BASE_SR = "https://studyriver.jp/wp-json/wp/v2/posts"
BASE_SS = "https://sassamahha.me/wp-json/wp/v2/posts"

LANGS_MAIN = [("ja", 10)]
LANGS_SUB  = [
    ("en", 3), ("es", 3), ("zhhans", 3), ("zhhant", 3),
    ("pt", 3), ("id", 3), ("fr", 3), ("it", 3), ("de", 3),
]
SASAKI      = ("ja", 7)

headers = {"User-Agent": "GitHubActionsFeedBot/1.0"}

def fetch(lang, limit, base):
    url = f"{base}?per_page={limit}&lang={lang}&_fields=title,link,lang"
    try:
        js = requests.get(url, headers=headers, timeout=10).json()
        # ✅ 言語が一致しているものだけを返す
        return [
            (p["title"]["rendered"], p["link"])
            for p in js
            if p.get("lang") == lang
        ][:limit]
    except Exception as e:
        print(f"[WARN] {lang} → {e}")
        return []


# ---------- フィード取得 ----------
sr_en  = fetch("en", 10, BASE_SR)
sr_sub = {code: fetch(code, n, BASE_SR) for code, n in LANGS_SUB}
ss_en  = fetch(*SASAKI, BASE_SS)

# ---------- Markdown ビルド ----------
md  = []
md.append("<!--　ここは手動でアイスブレイク分 -->\n")
md.append("## 📰 New feeds")

# Study River
md.append("### Study River")
for title, url in sr_en:
    md.append(f"- [{title}]({url})")

# Sasakiya Shoten
md.append("\n### Sasakiya Shoten")
for title, url in ss_en:
    md.append(f"- [{title}]({url})")

md.append("\n<!--　Roadto2112が完成次第挿入する -->\n")
md.append("---")
md.append("👇**Delivered in your language.**")

for code, _ in LANGS_SUB:
    label = {
        "en": "Japanese", "es": "Spanish",
        "zhhans": "Chinese (Simplified)", "zhhant": "Chinese (Traditional)",
        "pt": "Portuguese", "id": "Indonesian",
        "fr": "French", "it": "Italian", "de": "German",
    }[code]
    md.append(f"\n#### {label}")
    for title, url in sr_sub.get(code, []):
        md.append(f"- [{title}]({url})")

# ---------- ファイル書き込み ----------
out_path.write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"Wrote {out_path}")
