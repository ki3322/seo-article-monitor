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
    except Exception as e:
        print(f"    [Error] Failed to fetch {url}: {e}")
        return None


def get_scraped_items(source: Dict) -> List[ScrapedItem]:
    """通用網頁爬蟲 - 目前所有來源皆使用 RSS，此函式保留作為備用"""
    return []
