"""
Worker để tải video/audio trong thread riêng
"""
from PyQt6.QtCore import QThread, pyqtSignal
from typing import Optional
from app.core.downloader import VideoDownloader, AudioDownloader
from app.utils.helpers import format_bytes

class DownloadWorker(QThread):
    """Worker thread tải video YouTube"""
    
    # Signals
    progress = pyqtSignal(dict)   # Emit tiến độ tải
    success = pyqtSignal(str)     # Emit file path khi tải xong
    error = pyqtSignal(str)       # Emit lỗi
    finished = pyqtSignal()       # Emit khi hoàn thành
    
    def __init__(self,
                 url: str,
                 output_path: str,
                 download_type: str,  # "video" hoặc "audio"
                 quality: Optional[str] = None,
                 audio_format: Optional[str] = None,
                 audio_bitrate: Optional[str] = None,
                 ffmpeg_path: Optional[str] = None):
        super().__init__()
        
        self.url = url
        self.output_path = output_path
        self.download_type = download_type
        self.quality = quality or "best"
        self.audio_format = audio_format or "mp3"
        self.audio_bitrate = audio_bitrate or "192"
        self.ffmpeg_path = ffmpeg_path
        self._is_running = True
    
    def _progress_callback(self, data: dict) -> None:
        """Callback tiến độ tải"""
        if not self._is_running:
            return
        
        if data['status'] == 'downloading':
            total = data.get('total', 0)
            downloaded = data.get('downloaded', 0)
            speed = data.get('speed', 0)
            eta = data.get('eta', 0)
            
            percent = 0
            if total > 0:
                percent = int((downloaded / total) * 100)
            
            self.progress.emit({
                'percent': percent,
                'downloaded': format_bytes(downloaded),
                'total': format_bytes(total),
                'speed': format_bytes(speed) if speed else "0 B",
                'eta': eta,
                'status': 'downloading',
            })
        
        elif data['status'] == 'finished':
            self.progress.emit({
                'percent': 100,
                'status': 'finished',
            })
    
    def _log_callback(self, message: str) -> None:
        """Callback log"""
        if self._is_running:
            self.progress.emit({
                'status': 'log',
                'message': message,
            })
    
    def run(self) -> None:
        """Chạy tải trong thread"""
        try:
            if self.download_type == "video":
                self._download_video()
            elif self.download_type == "audio":
                self._download_audio()
            else:
                raise ValueError(f"Kiểu tải không hợp lệ: {self.download_type}")
        
        except Exception as e:
            if self._is_running:
                error_msg = str(e)
                
                # Xử lý lỗi cụ thể
                if "ffmpeg" in error_msg.lower():
                    self.error.emit("FFmpeg chưa được cài đặt. Vui lòng cài đặt FFmpeg.")
                elif "unavailable" in error_msg.lower():
                    self.error.emit("Video không khả dụng hoặc đã bị xóa.")
                elif "permission" in error_msg.lower():
                    self.error.emit("Lỗi quyền truy cập. Kiểm tra quyền thư mục đích.")
                elif "connection" in error_msg.lower() or "network" in error_msg.lower():
                    self.error.emit("Lỗi kết nối internet.")
                else:
                    self.error.emit(f"Lỗi: {error_msg}")
        
        finally:
            self.finished.emit()
    
    def _download_video(self) -> None:
        """Tải video"""
        downloader = VideoDownloader(
            self.output_path,
            progress_callback=self._progress_callback,
            log_callback=self._log_callback,
            ffmpeg_path=self.ffmpeg_path
        )
        
        file_path = downloader.download_video(self.url, self.quality)
        
        if self._is_running:
            self.success.emit(file_path)
    
    def _download_audio(self) -> None:
        """Tải audio"""
        downloader = AudioDownloader(
            self.output_path,
            progress_callback=self._progress_callback,
            log_callback=self._log_callback,
            ffmpeg_path=self.ffmpeg_path
        )
        
        file_path = downloader.download_audio(
            self.url,
            self.audio_format,
            self.audio_bitrate
        )
        
        if self._is_running:
            self.success.emit(file_path)
    
    def stop(self) -> None:
        """Dừng worker"""
        self._is_running = False
        self.wait()
