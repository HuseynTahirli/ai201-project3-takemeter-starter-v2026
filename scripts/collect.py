"""Collect r/playstation self posts via Reddit's official API (PRAW) for labeling.

Requires a Reddit "script" app (create one at https://www.reddit.com/prefs/apps)
and these environment variables set before running:
    REDDIT_CLIENT_ID
    REDDIT_CLIENT_SECRET
    REDDIT_USER_AGENT   (e.g. "takemeter-collector/0.1 by u/<your_username>")
"""

import csv
import os
import random

import praw

SUBREDDIT = "playstation"
LISTINGS = ["top", "hot", "new"]
MIN_SELFTEXT_LEN = 80
TARGET_COUNT = 260
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw_posts.csv")

BAD_SELFTEXT = {"[removed]", "[deleted]"}


def get_reddit():
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    user_agent = os.environ.get("REDDIT_USER_AGENT")
    if not all([client_id, client_secret, user_agent]):
        raise RuntimeError(
            "Missing REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET / REDDIT_USER_AGENT "
            "environment variables. Create a 'script' app at "
            "https://www.reddit.com/prefs/apps and set these before running."
        )
    return praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)


def iter_listing(subreddit, listing):
    if listing == "top":
        return subreddit.top(time_filter="year", limit=None)
    if listing == "hot":
        return subreddit.hot(limit=None)
    if listing == "new":
        return subreddit.new(limit=None)
    raise ValueError(listing)


def collect_posts(reddit):
    subreddit = reddit.subreddit(SUBREDDIT)
    seen_ids = set()
    seen_texts = set()
    posts = []

    for listing in LISTINGS:
        if len(posts) >= TARGET_COUNT:
            break
        for submission in iter_listing(subreddit, listing):
            if len(posts) >= TARGET_COUNT:
                break

            post_id = submission.id
            if post_id in seen_ids:
                continue
            if not submission.is_self:
                continue

            selftext = submission.selftext or ""
            if len(selftext) < MIN_SELFTEXT_LEN:
                continue
            if selftext.strip() in BAD_SELFTEXT:
                continue

            title = submission.title or ""
            text = f"{title}\n{selftext}"
            if text in seen_texts:
                continue

            seen_ids.add(post_id)
            seen_texts.add(text)
            posts.append({
                "id": post_id,
                "url": f"https://www.reddit.com{submission.permalink}",
                "text": text,
            })

    return posts


def save_posts(posts):
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "url", "text"])
        writer.writeheader()
        writer.writerows(posts)


def main():
    reddit = get_reddit()
    posts = collect_posts(reddit)
    save_posts(posts)

    print(f"Collected {len(posts)} posts -> {OUT_PATH}")

    sample = random.sample(posts, min(40, len(posts)))
    for i, post in enumerate(sample, 1):
        snippet = post["text"][:300].replace("\n", " / ")
        print(f"\n--- {i}. id={post['id']} ---")
        print(snippet)


if __name__ == "__main__":
    main()
