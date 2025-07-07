#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日本語向けフィード (RSS) 取得スクリプト
"""
import pathlib, datetime, feedparser

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "05.NewsLetter" / "ja"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TODAY = datetime.date.today()
fname = f"{TODAY.isoformat()}-newsletter.md"
out_path = OUTPUT_DIR / fname

# ---------- RSS 取得先 ----------
FEEDS = [
    ("Study River（スタリバ）", "https://studyriver.jp/feed/"),
    ("ささきや商店", "https://sassamahha.me/feed/"),
]

def fetch_rss(url, limit=7):
    entries = feedparser.parse(url).entries
    return [(entry.title, entry.link) for entry in entries[:limit]]

# ---------- Markdown 出力 ----------
md = []
md.append("## 📰 今週の記事はこちら")

for label, url in FEEDS:
    md.append(f"\n### {label}")
    try:
        items = fetch_rss(url)
        for title, link in items:
            md.append(f"- [{title}]({link})")
    except Exception as e:
        md.append(f"- ⚠️ フィード取得失敗: {label} ({e})")

out_path.write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"Wrote {out_path}")
