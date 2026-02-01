import json
import os
from typing import Optional
from config import STATE_FILE


class StateManager:
    def __init__(self, state_file: str = STATE_FILE):
        self.state_file = state_file
        self.state = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"last_seen": {}}

    def save(self) -> None:
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def get_last_seen(self, source_id: str) -> Optional[str]:
        return self.state.get("last_seen", {}).get(source_id)

    def set_last_seen(self, source_id: str, item_id: str) -> None:
        if "last_seen" not in self.state:
            self.state["last_seen"] = {}
        self.state["last_seen"][source_id] = item_id

    def is_seen(self, source_id: str, item_id: str) -> bool:
        seen_items = self.state.get("seen_items", {}).get(source_id, [])
        return item_id in seen_items

    def mark_seen(self, source_id: str, item_id: str, max_items: int = 100) -> None:
        if "seen_items" not in self.state:
            self.state["seen_items"] = {}
        if source_id not in self.state["seen_items"]:
            self.state["seen_items"][source_id] = []

        if item_id not in self.state["seen_items"][source_id]:
            self.state["seen_items"][source_id].append(item_id)
            # 保留最近的 max_items 筆記錄
            if len(self.state["seen_items"][source_id]) > max_items:
                self.state["seen_items"][source_id] = self.state["seen_items"][source_id][-max_items:]
