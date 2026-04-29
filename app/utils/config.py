"""
Cấu hình ứng dụng YouTube Downloader
"""
import os
import sys
import json
from pathlib import Path

def get_data_dir() -> Path:
    """Lấy thư mục data cho source hoặc bản build"""
    if getattr(sys, "frozen", False):
        base_dir = Path(os.getenv("APPDATA", str(Path.home()))) / "YouTube Downloader"
    else:
        base_dir = Path(__file__).resolve().parents[2] / "data"

    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir

DATA_DIR = get_data_dir()
CONFIG_FILE = DATA_DIR / "config.json"
HISTORY_FILE = DATA_DIR / "download_history.json"

# Cấu hình mặc định
DEFAULT_DOWNLOAD_PATH = str(Path.home() / "Downloads" / "YouTube Downloads")
DEFAULT_THEME = "light"  # light hoặc dark
DEFAULT_AUDIO_FORMAT = "mp3"
DEFAULT_AUDIO_BITRATE = "192"
DEFAULT_VIDEO_QUALITY = "best"

# Các tùy chọn video quality
VIDEO_QUALITIES = {
    "best": "Chất lượng tốt nhất",
    "360p": "360p",
    "480p": "480p",
    "720p": "720p",
    "1080p": "1080p",
    "2K": "2K (1440p)",
    "4K": "4K (2160p)",
}

# Các tùy chọn audio format
AUDIO_FORMATS = {
    "mp3": "MP3",
    "m4a": "M4A",
    "wav": "WAV",
}

# Các tùy chọn audio bitrate
AUDIO_BITRATES = {
    "128": "128 kbps",
    "192": "192 kbps",
    "320": "320 kbps",
}

# Cấu hình UI
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# Màu sắc
COLORS_LIGHT = {
    "bg": "#FFFFFF",
    "bg_secondary": "#F5F5F5",
    "text": "#1A1A1A",
    "text_secondary": "#666666",
    "border": "#E0E0E0",
    "primary": "#2196F3",
    "primary_hover": "#1976D2",
    "success": "#4CAF50",
    "error": "#F44336",
    "warning": "#FF9800",
}

COLORS_DARK = {
    "bg": "#1E1E1E",
    "bg_secondary": "#2D2D2D",
    "text": "#FFFFFF",
    "text_secondary": "#BBBBBB",
    "border": "#3D3D3D",
    "primary": "#42A5F5",
    "primary_hover": "#1E88E5",
    "success": "#66BB6A",
    "error": "#EF5350",
    "warning": "#FFA726",
}

def get_theme_colors(theme: str = DEFAULT_THEME) -> dict:
    """Lấy bảng màu theo theme"""
    if theme == "dark":
        return COLORS_DARK
    return COLORS_LIGHT

def load_config() -> dict:
    """Tải cấu hình đã lưu"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    
    return {
        "download_path": DEFAULT_DOWNLOAD_PATH,
        "theme": DEFAULT_THEME,
        "audio_format": DEFAULT_AUDIO_FORMAT,
        "audio_bitrate": DEFAULT_AUDIO_BITRATE,
        "video_quality": DEFAULT_VIDEO_QUALITY,
        "ffmpeg_path": "",  # Để trống để auto-detect
    }

def save_config(config: dict) -> None:
    """Lưu cấu hình"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
