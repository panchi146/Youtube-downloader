"""
Worker để phân tích video trong thread riêng
"""
from PyQt6.QtCore import QThread, pyqtSignal
from typing import Optional
from app.core.analyzer import VideoAnalyzer

class AnalyzeWorker(QThread):
    """Worker thread phân tích video YouTube"""
    
    # Signals
    success = pyqtSignal(dict)  # Emit khi phân tích thành công
    error = pyqtSignal(str)     # Emit khi có lỗi
    finished = pyqtSignal()     # Emit khi hoàn thành
    
    def __init__(self, url: str):
        super().__init__()
        self.url = url
        self.analyzer = VideoAnalyzer()
        self._is_running = True
    
    def run(self) -> None:
        """Chạy phân tích trong thread"""
        try:
            info = self.analyzer.analyze(self.url)
            
            if self._is_running and info:
                self.success.emit(info)
            
        except ValueError as e:
            if self._is_running:
                self.error.emit(f"Lỗi URL: {str(e)}")
        
        except Exception as e:
            if self._is_running:
                error_msg = str(e)
                
                # Xử lý lỗi cụ thể
                if "connection" in error_msg.lower() or "network" in error_msg.lower():
                    self.error.emit("Lỗi kết nối internet. Vui lòng kiểm tra kết nối.")
                elif "youtube" in error_msg.lower():
                    self.error.emit("Lỗi YouTube. Link có thể không hợp lệ hoặc video đã bị xóa.")
                else:
                    self.error.emit(f"Lỗi: {error_msg}")
        
        finally:
            self.finished.emit()
    
    def stop(self) -> None:
        """Dừng worker"""
        self._is_running = False
        self.wait()
