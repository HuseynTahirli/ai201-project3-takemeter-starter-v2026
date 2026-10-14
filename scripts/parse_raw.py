"""Parse saved Reddit search JSON pages in data/raw/ into data/raw_posts.csv."""
import csv
import glob
import html
import random
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAW_GLOB = "data/raw/*.json"
OUT_PATH = "data/raw_posts.csv"
TARGET_SUBREDDIT = "playstation"
MIN_SELFTEXT_LEN = 80
BLOCKED_SELFTEXT = {"[removed]", "[deleted]"}

import json


def load_posts():
    posts = []
    for path in sorted(glob.glob(RAW_GLOB)):
        with open(path, encoding="utf-8") as f:
            listing = json.load(f)
        for child in listing["data"]["children"]:
            posts.append(child["data"])
    return posts


def main():
    posts = load_posts()
    total = len(posts)
    print(f"Loaded {total} posts from {RAW_GLOB}")

    step = posts
    step = [p for p in step if p.get("subreddit") == TARGET_SUBREDDIT]
    print(f"  after subreddit == '{TARGET_SUBREDDIT}': {len(step)} (dropped {total - len(step)})")
    n = len(step)

    step = [p for p in step if p.get("is_self") is True]
    print(f"  after is_self: {len(step)} (dropped {n - len(step)})")
    n = len(step)

    step = [p for p in step if p.get("stickied") is False]
    print(f"  after not stickied: {len(step)} (dropped {n - len(step)})")
    n = len(step)

    step = [p for p in step if p.get("distinguished") is None]
    print(f"  after distinguished is None: {len(step)} (dropped {n - len(step)})")
    n = len(step)

    def ok_selftext(p):
        text = p.get("selftext") or ""
        if len(text) < MIN_SELFTEXT_LEN:
            return False
        if text.strip() in BLOCKED_SELFTEXT:
            return False
        return True

    step = [p for p in step if ok_selftext(p)]
    print(f"  after selftext length/placeholder filter: {len(step)} (dropped {n - len(step)})")
    n = len(step)

    seen_ids = set()
    seen_texts = set()
    deduped = []
    for p in step:
        pid = p["id"]
        title = html.unescape(p.get("title") or "")
        selftext = html.unescape(p.get("selftext") or "")
        text = title + "\n" + selftext
        if pid in seen_ids or text in seen_texts:
            continue
        seen_ids.add(pid)
        seen_texts.add(text)
        deduped.append((pid, p.get("url") or "", text))
    print(f"  after dedupe by id and exact text: {len(deduped)} (dropped {n - len(deduped)})")

    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "url", "text"])
        writer.writerows(deduped)

    print(f"\nFinal count: {len(deduped)} posts written to {OUT_PATH}")

    sample = deduped if len(deduped) <= 40 else random.sample(deduped, 40)
    print(f"\n--- {len(sample)} random posts (first 300 chars) ---")
    for pid, url, text in sample:
        print(f"\n[{pid}] {text[:300]!r}")

    print("\n--- Possible distinctions worth labelling on (not final labels) ---")
    print("1. Whether a specific, checkable fact (patch note, price, date, benchmark number) "
          "is doing the actual argumentative work, versus just being mentioned in passing.")
    print("2. Whether the post is about something that just happened to the writer "
          "(a purchase, a crash, a launch they just played) versus a general claim about "
          "the platform/industry with no time anchor.")
    print("3. Whether the post offers any support (evidence, comparison, reasoning) for its "
          "claim, or is a bare assertion of opinion.")
    print("4. Whether the post is asking a question / seeking help versus making a claim or "
          "argument at all.")


if __name__ == "__main__":
    main()
