import os

# Telegram 設定
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# RSSHub 實例 (用於 Twitter/X 監控)
RSSHUB_INSTANCE = "https://pkmnhbs.zeabur.app"

# RSS 來源 (網站)
RSS_SOURCES = [
    {
        "name": "Search Engine Journal",
        "url": "https://www.searchenginejournal.com/feed/",
        "type": "website",
    },
    {
        "name": "Search Engine Land",
        "url": "https://searchengineland.com/feed",
        "type": "website",
    },
]

# 網頁爬蟲來源 (無 RSS 的網站)
SCRAPE_SOURCES = []

# Twitter/X 帳號 (透過 RSSHub)
TWITTER_ACCOUNTS = [
    "JohnMu",
    "dannysullivan",
    "randfish",
]

# 狀態檔案路徑
STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")

# 請求設定
REQUEST_TIMEOUT = 30
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
