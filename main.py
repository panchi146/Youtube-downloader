"""
YouTube Downloader - Ứng dụng tải video/audio từ YouTube
"""
import sys
import subprocess
import ctypes
from pathlib import Path

# Thêm thư mục app vào path
APP_DIR = Path(__file__).parent
sys.path.insert(0, str(APP_DIR))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from app.ui.main_window import YouTubeDownloaderApp

if sys.platform == "win32":
    _old_popen = subprocess.Popen

    def _popen_no_console(*args, **kwargs):
        kwargs["creationflags"] = kwargs.get("creationflags", 0) | subprocess.CREATE_NO_WINDOW
        return _old_popen(*args, **kwargs)

    subprocess.Popen = _popen_no_console

def resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).parent / relative_path

def main():
    """Chương trình chính"""
    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "youtube.downloader.app"
        )

    app = QApplication(sys.argv)

    icon_path = resource_path("assets/icon.ico")
    app.setWindowIcon(QIcon(str(icon_path)))
    
    # Tạo và hiển thị cửa sổ chính
    window = YouTubeDownloaderApp()
    window.setWindowIcon(QIcon(str(icon_path)))
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
