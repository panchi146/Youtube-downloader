"""
Quản lý lịch sử tải xuống
"""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from app.utils.config import HISTORY_FILE

class DownloadHistory:
    """Quản lý lịch sử tải xuống"""
    
    def __init__(self):
        self.history_file = HISTORY_FILE
        self.history: List[Dict] = []
        self.load()
    
    def load(self) -> None:
        """Tải lịch sử từ file"""
        if self.history_file.exists():
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except Exception:
                self.history = []
        else:
            self.history = []
    
    def save(self) -> None:
        """Lưu lịch sử vào file"""
        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Lỗi khi lưu lịch sử: {e}")
    
    def add(self, 
            url: str,
            title: str,
            channel: str,
            duration: int,
            type_: str,  # "video" hoặc "audio"
            quality: str,
            format_: str,  # định dạng/chất lượng (mp3, 720p, etc)
            file_path: str,
            file_size: int) -> None:
        """Thêm một bản ghi tải xuống vào lịch sử"""
        
        entry = {
            "id": len(self.history) + 1,
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "title": title,
            "channel": channel,
            "duration": duration,
            "type": type_,
            "quality": quality,
            "format": format_,
            "file_path": file_path,
            "file_size": file_size,
            "status": "success"
        }
        
        self.history.insert(0, entry)
        self.save()
    
    def get_history(self) -> List[Dict]:
        """Lấy toàn bộ lịch sử"""
        return self.history
    
    def get_recent(self, limit: int = 10) -> List[Dict]:
        """Lấy các bản ghi gần đây"""
        return self.history[:limit]
    
    def clear_history(self) -> None:
        """Xóa toàn bộ lịch sử"""
        self.history = []
        self.save()
    
    def remove_entry(self, entry_id: int) -> None:
        """Xóa một bản ghi"""
        self.history = [h for h in self.history if h.get("id") != entry_id]
        self.save()
    
    def format_entry(self, entry: Dict) -> str:
        """Định dạng bản ghi để hiển thị"""
        try:
            timestamp = datetime.fromisoformat(entry["timestamp"])
            time_str = timestamp.strftime("%d/%m/%Y %H:%M:%S")
        except:
            time_str = "N/A"
        
        type_str = "Video" if entry["type"] == "video" else "Âm thanh"
        quality_str = entry.get("quality", entry.get("format", "N/A"))
        
        return f"{time_str} - {entry['title'][:50]} ({type_str} - {quality_str})"
