#!/usr/bin/env python3
"""Fetch RSS entries and write Markdown like:
---
### 各言語（LANG: EN）
- https://...
"""
import datetime, pathlib, feedparser

# ---------- 設定 ----------
TODAY = datetime.date.today().isoformat()
POSTS = 5

# Study River
SR_LANGS = ["ja", "en", "es", "pt", "fr", "it", "de", "zh", "zh-hant", "ko", "id"]
def sr_feed(lang):
    return f"https://studyriver.jp/{'' if lang=='ja' else lang+'/'}feed"

# Sasakiya Shoten
FEEDS = {
    **{lang: sr_feed(lang) for lang in SR_LANGS},
    "sasakiya-ja": "https://sassamahha.me/feed",
    "sasakiya-en": "https://sassamahha.me/en/feed",
}
# --------------------------

out_dir = pathlib.Path("feeds")
out_dir.mkdir(exist_ok=True)
md_path = out_dir / f"{TODAY}.md"

lines = ["---"]

for label, url in FEEDS.items():
    fp = feedparser.parse(url)
    if not fp.entries:
        continue

    # LANG 表示を作成
    lang_tag = label.split("-")[-1].upper() if label.startswith("sasakiya") else label.upper()
    header = f"### 各言語（LANG: {lang_tag}）"
    lines.append(header)

    # 各記事 URL だけを列挙
    for entry in fp.entries[:POSTS]:
        link = entry.get("link", "#")
        lines.append(f"- {link}")
    lines.append("")           # 空行

md_path.write_text("\n".join(lines), encoding="utf-8")
print(f"✅  wrote {md_path}")
