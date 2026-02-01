import requests
from bs4 import BeautifulSoup
import hashlib
from typing import List, Dict, Optional
from dataclasses import dataclass
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config import REQUEST_TIMEOUT, USER_AGENT


@dataclass
class ScrapedItem:
    id: str
    title: str
    link: str
    source: str
    source_type: str = "website"


def generate_item_id(link: str, title: str) -> str:
    content = f"{link}:{title}"
    return hashlib.md5(content.encode()).hexdigest()[:16]


def fetch_page(url: str) -> Optional[BeautifulSoup]:
    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception:
        return None


def scrape_pokemon_center_online(source: Dict) -> List[ScrapedItem]:
    items = []
    soup = fetch_page(source["url"])

    if soup is None:
        return items

    # Pokemon Center Online 新聞頁面結構
    # 嘗試尋找新聞文章連結
    for article in soup.select("article, .news-item, .news-list li, a[href*='news']")[:10]:
        link_tag = article if article.name == "a" else article.find("a")
        if not link_tag or not link_tag.get("href"):
            continue

        link = link_tag.get("href", "")
        if not link.startswith("http"):
            link = "https://www.pokemoncenter-online.com" + link

        title_tag = article.find(["h2", "h3", "h4", ".title", "p"])
        title = title_tag.get_text(strip=True) if title_tag else link_tag.get_text(strip=True)

        if not title:
            continue

        item_id = generate_item_id(link, title)
        items.append(ScrapedItem(
            id=item_id,
            title=title[:100] + "..." if len(title) > 100 else title,
            link=link,
            source=source["name"],
        ))

    return items


def scrape_pokemon_infomation(source: Dict) -> List[ScrapedItem]:
    items = []
    soup = fetch_page(source["url"])

    if soup is None:
        return items

    # Pokemon Information 網站結構
    for article in soup.select("article, .post, .entry, a[href*='post'], .news-item")[:10]:
        link_tag = article if article.name == "a" else article.find("a")
        if not link_tag or not link_tag.get("href"):
            continue

        link = link_tag.get("href", "")
        if not link.startswith("http"):
            link = "https://pokemon-infomation.com" + link

        title_tag = article.find(["h2", "h3", "h4", ".entry-title", ".post-title"])
        title = title_tag.get_text(strip=True) if title_tag else link_tag.get_text(strip=True)

        if not title:
            continue

        item_id = generate_item_id(link, title)
        items.append(ScrapedItem(
            id=item_id,
            title=title[:100] + "..." if len(title) > 100 else title,
            link=link,
            source=source["name"],
        ))

    return items


def get_scraped_items(source: Dict) -> List[ScrapedItem]:
    url = source.get("url", "")

    if "pokemoncenter-online.com" in url:
        return scrape_pokemon_center_online(source)
    elif "pokemon-infomation.com" in url:
        return scrape_pokemon_infomation(source)

    return []
