"""
Phân tích thông tin video YouTube
"""
import yt_dlp
from typing import Dict, Optional
from app.utils.helpers import is_valid_youtube_url, get_ffmpeg_bin_path

class VideoAnalyzer:
    """Phân tích thông tin video YouTube"""
    
    def __init__(self):
        self.ydl_opts = {
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'socket_timeout': 30,
        }

        ffmpeg_bin = get_ffmpeg_bin_path()
        if ffmpeg_bin:
            self.ydl_opts['ffmpeg_location'] = ffmpeg_bin
    
    def analyze(self, url: str) -> Optional[Dict]:
        """
        Phân tích link YouTube và lấy thông tin
        
        Returns:
            Dict chứa thông tin video hoặc None nếu lỗi
        """
        if not is_valid_youtube_url(url):
            raise ValueError("URL không phải là link YouTube hợp lệ")
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    "title": info.get("title", "Unknown"),
                    "channel": info.get("uploader", "Unknown"),
                    "duration": info.get("duration", 0),
                    "thumbnail": info.get("thumbnail", ""),
                    "description": info.get("description", ""),
                    "view_count": info.get("view_count", 0),
                    "upload_date": info.get("upload_date", ""),
                    "formats": info.get("formats", []),
                    "ext": info.get("ext", ""),
                }
        
        except yt_dlp.utils.DownloadError as e:
            raise ValueError(f"Video không tìm thấy hoặc không khả dụng: {str(e)}")
        except Exception as e:
            raise Exception(f"Lỗi khi phân tích video: {str(e)}")
    
    def get_available_formats(self, info: Dict) -> Dict:
        """
        Lấy các format khả dụng từ thông tin video
        
        Returns:
            Dict chứa video formats và audio formats
        """
        formats = info.get("formats", [])
        
        video_formats = []
        audio_formats = []
        
        for fmt in formats:
            if fmt.get("vcodec") != "none" and fmt.get("acodec") != "none":
                # Video có âm thanh
                height = fmt.get("height")
                if height:
                    video_formats.append({
                        "format_id": fmt.get("format_id"),
                        "height": height,
                        "width": fmt.get("width"),
                        "ext": fmt.get("ext"),
                        "filesize": fmt.get("filesize"),
                    })
            elif fmt.get("vcodec") != "none":
                # Video không có âm thanh
                height = fmt.get("height")
                if height:
                    video_formats.append({
                        "format_id": fmt.get("format_id"),
                        "height": height,
                        "width": fmt.get("width"),
                        "ext": fmt.get("ext"),
                        "filesize": fmt.get("filesize"),
                    })
            elif fmt.get("acodec") != "none":
                # Audio
                audio_formats.append({
                    "format_id": fmt.get("format_id"),
                    "abr": fmt.get("abr"),
                    "ext": fmt.get("ext"),
                    "filesize": fmt.get("filesize"),
                })
        
        return {
            "video_formats": video_formats,
            "audio_formats": audio_formats,
        }
