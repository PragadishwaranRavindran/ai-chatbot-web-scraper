import json
import os
from typing import Dict, Any

DEFAULT_CONFIG: Dict[str, Any] = {
    "app_title": "AI Chatbot",
}

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")


def load_config() -> Dict[str, Any]:
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            file_cfg = json.load(f)
            # Merge with defaults to ensure missing keys are provided
            merged = {**DEFAULT_CONFIG, **(file_cfg or {})}
            return merged
    except Exception:
        # File missing or invalid JSON → use defaults
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]) -> Dict[str, Any]:
    data = {**DEFAULT_CONFIG, **(config or {})}
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return data
