"""
Tải video/audio từ YouTube
"""
import yt_dlp
import os
from pathlib import Path
from typing import Callable, Optional
from app.utils.helpers import (
    get_video_format_by_quality,
    ensure_dir_exists,
    get_safe_filename,
    get_ffmpeg_bin_path,
)

class VideoDownloader:
    """Tải video từ YouTube"""
    
    def __init__(self, 
                 output_path: str,
                 progress_callback: Optional[Callable] = None,
                 log_callback: Optional[Callable] = None,
                 ffmpeg_path: Optional[str] = None):
        """
        Khởi tạo downloader
        
        Args:
            output_path: Đường dẫn lưu video
            progress_callback: Callback để cập nhật tiến độ
            log_callback: Callback để ghi log
            ffmpeg_path: Đường dẫn đến FFmpeg (nếu None, sẽ auto-detect)
        """
        self.output_path = output_path
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.current_file_path = None
        
        # Xác định đường dẫn FFmpeg (ưu tiên portable)
        self.ffmpeg_bin = get_ffmpeg_bin_path()
        
        ensure_dir_exists(output_path)
    
    def _log(self, message: str) -> None:
        """Ghi log"""
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)
    
    def _progress_hook(self, d) -> None:
        """Hook xử lý tiến độ tải"""
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes', 0)
            downloaded_bytes = d.get('downloaded_bytes', 0)
            speed = d.get('speed', 0)
            eta = d.get('eta', 0)
            
            if self.progress_callback:
                progress_data = {
                    'status': 'downloading',
                    'total': total_bytes,
                    'downloaded': downloaded_bytes,
                    'speed': speed,
                    'eta': eta,
                    'filename': d.get('filename', ''),
                }
                self.progress_callback(progress_data)
        
        elif d['status'] == 'finished':
            self.current_file_path = d.get('filename')
            if self.progress_callback:
                self.progress_callback({
                    'status': 'finished',
                    'filename': self.current_file_path,
                })
    
    def download_video(self, url: str, quality: str = "best") -> str:
        """
        Tải video
        
        Args:
            url: URL YouTube
            quality: Chất lượng video (best, 360p, 480p, 720p, 1080p, 2K, 4K)
        
        Returns:
            Đường dẫn file đã tải
        """
        
        format_spec = get_video_format_by_quality(quality)
        
        # Chuẩn bị ydl_opts
        ydl_opts = {
            'format': format_spec,
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook],
            'quiet': False,
            'no_warnings': False,
            'socket_timeout': 30,
            'merge_output_format': 'mp4',
        }
        
        # Thêm ffmpeg_location nếu tìm thấy
        if self.ffmpeg_bin:
            ydl_opts['ffmpeg_location'] = self.ffmpeg_bin
        
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                self._log(f"Tải xong: {file_path}")
                return file_path
        
        except Exception as e:
            self._log(f"Lỗi tải video: {str(e)}")
            raise

class AudioDownloader:
    """Tải audio từ YouTube"""
    
    def __init__(self,
                 output_path: str,
                 progress_callback: Optional[Callable] = None,
                 log_callback: Optional[Callable] = None,
                 ffmpeg_path: Optional[str] = None):
        """
        Khởi tạo audio downloader
        
        Args:
            output_path: Đường dẫn lưu audio
            progress_callback: Callback để cập nhật tiến độ
            log_callback: Callback để ghi log
            ffmpeg_path: Đường dẫn đến FFmpeg (nếu None, sẽ auto-detect)
        """
        self.output_path = output_path
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.current_file_path = None
        
        # Xác định đường dẫn FFmpeg (ưu tiên portable)
        self.ffmpeg_bin = get_ffmpeg_bin_path()
        
        ensure_dir_exists(output_path)
    
    def _log(self, message: str) -> None:
        """Ghi log"""
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)
    
    def _progress_hook(self, d) -> None:
        """Hook xử lý tiến độ tải"""
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes', 0)
            downloaded_bytes = d.get('downloaded_bytes', 0)
            speed = d.get('speed', 0)
            eta = d.get('eta', 0)
            
            if self.progress_callback:
                progress_data = {
                    'status': 'downloading',
                    'total': total_bytes,
                    'downloaded': downloaded_bytes,
                    'speed': speed,
                    'eta': eta,
                    'filename': d.get('filename', ''),
                }
                self.progress_callback(progress_data)
        
        elif d['status'] == 'finished':
            self.current_file_path = d.get('filename')
            if self.progress_callback:
                self.progress_callback({
                    'status': 'finished',
                    'filename': self.current_file_path,
                })
    
    def download_audio(self, 
                      url: str,
                      audio_format: str = "mp3",
                      bitrate: str = "192") -> str:
        """
        Tải audio
        
        Args:
            url: URL YouTube
            audio_format: Định dạng audio (mp3, m4a, wav)
            bitrate: Bitrate audio (128, 192, 320)
        
        Returns:
            Đường dẫn file đã tải
        """
        
        # Ánh xạ định dạng
        format_ext = {
            'mp3': 'mp3',
            'm4a': 'm4a',
            'wav': 'wav',
        }.get(audio_format, 'mp3')
        
        # Tùy chọn yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': bitrate,
            }],
            'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook],
            'quiet': False,
            'no_warnings': False,
            'socket_timeout': 30,
        }
        
        # Thêm ffmpeg_location nếu tìm thấy
        if self.ffmpeg_bin:
            ydl_opts['ffmpeg_location'] = self.ffmpeg_bin
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                # File đã được chuyển đổi
                expected_file = os.path.join(
                    self.output_path,
                    f"{info['title']}.{format_ext}"
                )
                self._log(f"Tải xong: {expected_file}")
                return expected_file
        
        except Exception as e:
            self._log(f"Lỗi tải audio: {str(e)}")
            raise
