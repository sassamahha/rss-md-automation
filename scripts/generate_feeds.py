#!/usr/bin/env python3
"""
Fetch RSS feeds and write to feeds/YYYY-MM-DD.md

Format:
---
### 各言語（LANG: EN）
- https://...
"""
import datetime, pathlib, feedparser

# ====== 設定 ======
TODAY = datetime.date.today().isoformat()
POSTS = 5

# Study River languages you publish
SR_LANGS = ["ja", "en", "es", "pt", "fr", "it", "de", "zh", "zh-hant", "ko", "id"]
def sr_feed(lang):
    return f"https://studyriver.jp/{'' if lang=='ja' else lang+'/'}feed"

# Feeds dict: {label: url}
FEEDS = {
    **{lang: sr_feed(lang) for lang in SR_LANGS},
    "sasakiya-ja": "https://sassamahha.me/feed",
    "sasakiya-en": "https://sassamahha.me/en/feed",
}
# ===================

out_dir = pathlib.Path("feeds")
out_dir.mkdir(exist_ok=True)
md_path = out_dir / f"{TODAY}.md"

lines = ["---"]

for label, url in FEEDS.items():
    fp = feedparser.parse(url)
    if not fp.entries:
        continue

    lang = key.split("-")[-1].upper() if key.startswith("sasakiya") else key.upper()
    lines.append(f"### LANG: {lang}")

    for e in fp.entries[:POSTS]:
        title = textwrap.shorten(e.get("title", "No title"), width=120)
        link  = e.get("link", "#")
        lines.append(f"- [{title}]({link})")
    lines.append("")

md_path.write_text("\n".join(lines), encoding="utf-8")
print(f"✅ wrote {md_path}")
