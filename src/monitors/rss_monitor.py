import feedparser
import hashlib
from typing import List, Dict, Optional
from dataclasses import dataclass
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config import NITTER_INSTANCES, REQUEST_TIMEOUT, USER_AGENT


@dataclass
class FeedItem:
    id: str
    title: str
    link: str
    source: str
    source_type: str  # 'website' or 'twitter'


def generate_item_id(link: str, title: str) -> str:
    content = f"{link}:{title}"
    return hashlib.md5(content.encode()).hexdigest()[:16]


def fetch_rss(url: str) -> Optional[feedparser.FeedParserDict]:
    try:
        feed = feedparser.parse(
            url,
            request_headers={"User-Agent": USER_AGENT},
        )
        if feed.bozo and not feed.entries:
            return None
        return feed
    except Exception:
        return None


def get_rss_items(source: Dict) -> List[FeedItem]:
    items = []
    feed = fetch_rss(source["url"])

    if feed is None or not feed.entries:
        return items

    for entry in feed.entries[:10]:  # 只處理最新 10 筆
        item_id = generate_item_id(
            entry.get("link", ""),
            entry.get("title", "")
        )
        items.append(FeedItem(
            id=item_id,
            title=entry.get("title", "無標題"),
            link=entry.get("link", ""),
            source=source["name"],
            source_type=source.get("type", "website"),
        ))

    return items


def get_twitter_items(username: str) -> List[FeedItem]:
    items = []

    for instance in NITTER_INSTANCES:
        url = f"{instance}/{username}/rss"
        feed = fetch_rss(url)

        if feed is not None and feed.entries:
            for entry in feed.entries[:10]:
                # Nitter RSS 的 title 通常是推文內容
                title = entry.get("title", "")
                if len(title) > 100:
                    title = title[:97] + "..."

                item_id = generate_item_id(
                    entry.get("link", ""),
                    entry.get("title", "")
                )

                # 轉換 Nitter 連結為 Twitter 連結
                link = entry.get("link", "")
                if instance in link:
                    link = link.replace(instance, "https://twitter.com")

                items.append(FeedItem(
                    id=item_id,
                    title=title,
                    link=link,
                    source=f"@{username}",
                    source_type="twitter",
                ))
            break  # 成功獲取後跳出迴圈

    return items
