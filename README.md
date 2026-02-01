# Pokemon Monitor

自動監控 Pokemon 相關網站和 Twitter 帳號，有新內容時透過 Telegram 發送通知。

## 監控目標

### 網站
- Pokemon GO Hub (https://pokemongohub.net/)
- Pokemon Center Online (https://www.pokemoncenter-online.com/)
- Pokemon Information (https://pokemon-infomation.com/)
- Serebii.net (https://www.serebii.net/)

### Twitter 帳號
- @PokemonGoApp
- @Zabi_pokeka
- @pokecamatomeru
- @UniteVids
- @pokerapidinfo
- @pokepoke_GW
- @pokemongoappko
- @snkrdunk_akiba

## 設定步驟

### 1. 建立 Telegram Bot

1. 在 Telegram 中搜尋 @BotFather
2. 發送 `/newbot` 並依照指示建立機器人
3. 記下 Bot Token（格式：`123456789:ABC-DEF...`）
4. 與你的 Bot 開啟對話，發送任意訊息
5. 取得你的 Chat ID：
   - 訪問 `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - 找到 `"chat":{"id":123456789}` 中的數字

### 2. 設定 GitHub Secrets

在你的 GitHub repository 中：

1. 前往 **Settings** → **Secrets and variables** → **Actions**
2. 點擊 **New repository secret**
3. 新增以下 secrets：
   - `TELEGRAM_BOT_TOKEN`: 你的 Bot Token
   - `TELEGRAM_CHAT_ID`: 你的 Chat ID

### 3. 啟用 GitHub Actions

1. 前往 repository 的 **Actions** 頁面
2. 啟用 workflows（如果需要的話）
3. 可以手動點擊 **Run workflow** 測試

## 本地執行

```bash
# 安裝依賴
pip install -r requirements.txt

# 設定環境變數
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"

# 執行
python src/main.py
```

## 專案結構

```
pokemon-monitor/
├── .github/workflows/monitor.yml  # GitHub Actions 設定
├── src/
│   ├── main.py                    # 主程式
│   ├── state.py                   # 狀態管理
│   ├── notifier.py                # Telegram 通知
│   └── monitors/
│       ├── rss_monitor.py         # RSS 監控
│       └── web_scraper.py         # 網頁爬蟲
├── config.py                      # 設定檔
├── state.json                     # 已讀記錄
└── requirements.txt               # Python 依賴
```

## 自訂監控目標

編輯 `config.py` 檔案：

- `RSS_SOURCES`: RSS feed 來源
- `SCRAPE_SOURCES`: 需要爬蟲的網站
- `TWITTER_ACCOUNTS`: Twitter 帳號列表

## 注意事項

- Twitter 監控透過 Nitter 實例，可能偶爾不穩定
- 網頁爬蟲可能因網站改版而需要調整
- GitHub Actions 免費帳號每月有 2000 分鐘執行限制
