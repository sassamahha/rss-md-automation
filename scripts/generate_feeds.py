#!/usr/bin/env python3
import datetime, pathlib, feedparser, textwrap

TODAY = datetime.date.today().isoformat()
POSTS = 5

# --- Feed 定義 ---
SR_LANGS = ["ja", "en", "es", "pt", "fr", "it", "de", "zh", "zh-hant", "ko", "id"]
def sr_feed(lang): return f"https://studyriver.jp/{'' if lang=='ja' else lang+'/'}feed"

FEEDS = {
    **{lang: sr_feed(lang) for lang in SR_LANGS},
    "sasakiya-ja": "https://sassamahha.me/feed",
    "sasakiya-en": "https://sassamahha.me/en/feed",
}
# ------------------

out_dir = pathlib.Path("feeds")
out_dir.mkdir(exist_ok=True)
md_path = out_dir / f"{TODAY}.md"

lines = ["---"]

for key, url in FEEDS.items():                  # ← key はこのループ内でのみ使用
    fp = feedparser.parse(url)
    if not fp.entries:
        continue

    lang = key.split("-")[-1].upper() if key.startswith("sasakiya") else key.upper()
    lines.append(f"### LANG: {lang}")

    for e in fp.entries[:POSTS]:
        title = textwrap.shorten(e.get("title", "No title"), width=120)
        link  = e.get("link", "#")
        lines.append(f"- [{title}]({link})")
    lines.append("")                            # 空行を入れる

md_path.write_text("\n".join(lines), encoding="utf-8")
print("✅ wrote", md_path)
