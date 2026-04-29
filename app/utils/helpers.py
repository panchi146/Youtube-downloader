"""
Các hàm tiện ích
"""
import re
import sys
import subprocess
from datetime import timedelta
from pathlib import Path

def format_bytes(bytes_size: float) -> str:
    """Chuyển đổi bytes thành định dạng dễ đọc"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def format_seconds(seconds: int) -> str:
    """Chuyển đổi giây thành định dạng HH:MM:SS"""
    return str(timedelta(seconds=int(seconds)))

def is_valid_youtube_url(url: str) -> bool:
    """Kiểm tra xem URL có phải YouTube không"""
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
    return bool(re.match(youtube_regex, url.strip()))

def get_safe_filename(filename: str) -> str:
    """Loại bỏ các ký tự không hợp lệ khỏi tên file"""
    invalid_chars = r'[<>:"/\\|?*]'
    return re.sub(invalid_chars, '_', filename).strip()

def ensure_dir_exists(path: str) -> bool:
    """Đảm bảo thư mục tồn tại"""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False

def get_app_base_dir() -> Path:
    """Lấy thư mục gốc khi chạy source hoặc bản build"""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parents[2]

def get_ffmpeg_bin_path() -> str:
    """Lấy thư mục ffmpeg/bin từ các vị trí portable"""
    base_dir = get_app_base_dir()

    candidates = [
        base_dir / "ffmpeg" / "bin",
        base_dir / "_internal" / "ffmpeg" / "bin",
    ]

    for path in candidates:
        if (path / "ffmpeg.exe").exists():
            return str(path)

    return ""

def check_ffmpeg_installed() -> bool:
    """Kiểm tra FFmpeg portable hoặc trong PATH"""
    ffmpeg_bin = get_ffmpeg_bin_path()

    if ffmpeg_bin:
        return True

    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception:
        return False

def get_video_format_by_quality(quality: str) -> str:
    """Lấy format code từ chất lượng"""
    quality_formats = {
       "best": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "4K": "bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/best[height<=2160]",
        "2K": "bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/best[height<=1440]",
        "1080p": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
        "720p": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]",
        "480p": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]",
        "360p": "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360]",
    }
    return quality_formats.get(quality, "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best")
