"""
Cửa sổ chính ứng dụng YouTube Downloader
"""
import os
from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QProgressBar, QStackedWidget, QTableWidget,
    QTableWidgetItem, QFileDialog, QMessageBox, QFrame, QScrollArea,
    QSpinBox, QTextEdit, QButtonGroup
)
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtNetwork import QNetworkAccessManager
from PyQt6.QtCore import QUrl
import requests

from app.ui.styles import get_stylesheet
from app.core.history import DownloadHistory
from app.utils.config import (
    load_config, save_config, WINDOW_WIDTH, WINDOW_HEIGHT,
    WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT, VIDEO_QUALITIES,
    AUDIO_FORMATS, AUDIO_BITRATES, DEFAULT_DOWNLOAD_PATH,
    get_theme_colors, DEFAULT_THEME
)
from app.utils.helpers import (
    format_bytes, format_seconds, is_valid_youtube_url,
    check_ffmpeg_installed, ensure_dir_exists,
    get_ffmpeg_bin_path
)
from app.workers.analyze_worker import AnalyzeWorker
from app.workers.download_worker import DownloadWorker

class YouTubeDownloaderApp(QMainWindow):
    """Ứng dụng tải video YouTube chính"""
    
    def __init__(self):
        super().__init__()
        
        # Tải cấu hình
        self.config = load_config()
        self.theme = self.config.get("theme", DEFAULT_THEME)
        self.colors = get_theme_colors(self.theme)
        
        # Khởi tạo lịch sử
        self.history = DownloadHistory()
        
        # Workers
        self.analyze_worker: Optional[AnalyzeWorker] = None
        self.download_worker: Optional[DownloadWorker] = None
        
        # Thông tin video hiện tại
        self.current_video_info: Optional[dict] = None
        self.last_downloaded_file: str = ""
        
        # Thiết lập cửa sổ
        self._setup_window()
        
        # Tạo UI
        self._create_ui()
        
        # Áp dụng stylesheet
        self.setStyleSheet(get_stylesheet(self.theme))
        
        # Kiểm tra FFmpeg
        self._check_ffmpeg()
    
    def _setup_window(self) -> None:
        """Thiết lập cửa sổ chính"""
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

    def _show_message(self, title: str, text: str, icon: QMessageBox.Icon) -> None:
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        if self.theme == "light":
            msg.setStyleSheet(
                """
                QMessageBox {
                    background-color: #ffffff;
                    color: #111111;
                }
                QMessageBox QLabel {
                    color: #111111;
                    background-color: transparent;
                }
                QMessageBox QPushButton {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #000000;
                    border-radius: 5px;
                    padding: 4px 16px;
                    min-width: 70px;
                    min-height: 24px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #f2f2f2;
                }
                QMessageBox QPushButton:pressed {
                    background-color: #e6e6e6;
                }
                """
            )
        else:
            msg.setStyleSheet(
                """
                QMessageBox {
                    background-color: #1e1e1e;
                    color: #ffffff;
                }
                QMessageBox QLabel {
                    color: #ffffff;
                    background-color: transparent;
                }
                QMessageBox QPushButton {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    border: 1px solid #ffffff;
                    border-radius: 5px;
                    padding: 4px 16px;
                    min-width: 70px;
                    min-height: 24px;
                }
                """
            )

        msg.exec()

    def show_warning(self, title: str, text: str) -> None:
        self._show_message(title, text, QMessageBox.Icon.Warning)

    def show_info(self, title: str, text: str) -> None:
        self._show_message(title, text, QMessageBox.Icon.Information)

    def show_error(self, title: str, text: str) -> None:
        self._show_message(title, text, QMessageBox.Icon.Critical)
    
    def _create_ui(self) -> None:
        """Tạo giao diện"""
        main_widget = QWidget()
        main_widget.setObjectName("centralWidget")
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tạo sidebar
        self.sidebar = self._create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Tạo content area
        self.page_stack = QStackedWidget()
        self.page_stack.setObjectName("mainContent")
        main_layout.addWidget(self.page_stack)
        
        # Thêm tabs
        self.home_tab = self._create_home_tab()
        self.history_tab = self._create_history_tab()
        self.settings_tab = self._create_settings_tab()
        
        self.page_stack.addWidget(self.home_tab)
        self.page_stack.addWidget(self.history_tab)
        self.page_stack.addWidget(self.settings_tab)
        
        # Cài đặt layout
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)

        self._set_active_nav(0)
    
    def _create_sidebar(self) -> QFrame:
        """Tạo sidebar"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            #sidebar {
                background-color: """ + self.colors['bg_secondary'] + """;
                border-right: 1px solid """ + self.colors['border'] + """;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("YouTube")
        title.setObjectName("sidebarTitle")
        layout.addWidget(title)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Downloader Pro")
        subtitle.setObjectName("sidebarSubtitle")
        layout.addWidget(subtitle)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(20)
        
        # Navigation buttons
        self.nav_home_btn = self._create_nav_button("🏠 Trang chính", 0)
        self.nav_history_btn = self._create_nav_button("📋 Lịch sử", 1)
        self.nav_settings_btn = self._create_nav_button("⚙️ Cài đặt", 2)
        
        layout.addWidget(self.nav_home_btn)
        layout.addWidget(self.nav_history_btn)
        layout.addWidget(self.nav_settings_btn)
        
        layout.addStretch()
        
        # Version info
        version_label = QLabel("v1.0.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 8pt;")
        layout.addWidget(version_label)
        
        return sidebar
    
    def _create_nav_button(self, text: str, tab_index: int) -> QPushButton:
        """Tạo nút navigation"""
        btn = QPushButton(text)
        btn.setProperty("nav", True)
        btn.setMinimumHeight(45)
        btn.clicked.connect(lambda: self._on_nav_clicked(tab_index))
        return btn

    def _on_nav_clicked(self, tab_index: int) -> None:
        """Chuyển trang và cập nhật trạng thái sidebar"""
        self.page_stack.setCurrentIndex(tab_index)
        self._set_active_nav(tab_index)

    def _set_active_nav(self, tab_index: int) -> None:
        """Đánh dấu nút sidebar đang active"""
        for index, btn in enumerate([self.nav_home_btn, self.nav_history_btn, self.nav_settings_btn]):
            btn.setProperty("active", index == tab_index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
    
    def _create_home_tab(self) -> QWidget:
        """Tạo tab trang chính"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setObjectName("scrollArea")
        scroll.viewport().setObjectName("scrollViewport")

        tab = QWidget()
        tab.setMinimumWidth(720)
        tab.setObjectName("scrollContent")
        scroll.setWidget(tab)

        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # URL input
        url_label = QLabel("Link YouTube:")
        url_label.setProperty("type", "title")
        layout.addWidget(url_label)
        
        input_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Dán link YouTube tại đây...")
        self.analyze_btn = QPushButton("🔍 Phân tích link")
        self.analyze_btn.setObjectName("primaryButton")
        self.analyze_btn.setMinimumWidth(150)
        self.analyze_btn.clicked.connect(self._on_analyze_clicked)
        self.reset_btn = QPushButton("✖ Xóa")
        self.reset_btn.setObjectName("outlineButton")
        self.reset_btn.setMinimumWidth(90)
        self.reset_btn.setMaximumWidth(90)
        self.reset_btn.clicked.connect(self._on_reset_clicked)
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.analyze_btn)
        input_layout.addWidget(self.reset_btn)
        layout.addLayout(input_layout)
        
        # Video info frame
        info_frame = QFrame()
        info_frame.setObjectName("card")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(12)
        
        # Thumbnail + Info
        info_top_layout = QHBoxLayout()
        
        # Thumbnail
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(220, 124)
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.setObjectName("thumbnail")
        self.thumbnail_label.setText("Chưa có thumbnail")
        info_top_layout.addWidget(self.thumbnail_label)
        
        # Video details
        details_layout = QVBoxLayout()
        
        self.title_label = QLabel("Chưa phân tích")
        self.title_label.setWordWrap(True)
        self.title_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.title_label.setObjectName("video_title")
        details_layout.addWidget(self.title_label)
        
        self.channel_label = QLabel()
        self.channel_label.setProperty("type", "secondary")
        details_layout.addWidget(self.channel_label)
        
        self.duration_label = QLabel()
        self.duration_label.setProperty("type", "secondary")
        details_layout.addWidget(self.duration_label)

        self.max_quality_label = QLabel("Chất lượng tối đa: -")
        self.max_quality_label.setProperty("type", "secondary")
        details_layout.addWidget(self.max_quality_label)

        self.size_label = QLabel("Dung lượng ước tính: -")
        self.size_label.setProperty("type", "secondary")
        details_layout.addWidget(self.size_label)
        
        details_layout.addStretch()
        
        info_top_layout.addLayout(details_layout, 1)
        info_layout.addLayout(info_top_layout)
        
        layout.addWidget(info_frame)
        
        # Download options
        options_frame = QFrame()
        options_frame.setObjectName("card")
        options_layout = QVBoxLayout(options_frame)
        options_layout.setSpacing(10)

        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Loại tải:"))

        self.type_video_radio = QPushButton("🎬 Video")
        self.type_video_radio.setCheckable(True)
        self.type_video_radio.setChecked(True)
        self.type_video_radio.setObjectName("toggleButton")
        self.type_video_radio.setMinimumWidth(120)
        self.type_video_radio.setMaximumWidth(140)

        self.type_audio_radio = QPushButton("🎵 Âm thanh")
        self.type_audio_radio.setCheckable(True)
        self.type_audio_radio.setObjectName("toggleButton")
        self.type_audio_radio.setMinimumWidth(130)
        self.type_audio_radio.setMaximumWidth(140)

        self.download_type_group = QButtonGroup(self)
        self.download_type_group.setExclusive(True)
        self.download_type_group.addButton(self.type_video_radio)
        self.download_type_group.addButton(self.type_audio_radio)
        self.download_type_group.buttonClicked.connect(self._on_type_changed)

        type_layout.addWidget(self.type_video_radio)
        type_layout.addWidget(self.type_audio_radio)
        type_layout.addStretch()
        options_layout.addLayout(type_layout)

        self.quality_widget = QWidget()
        quality_layout = QHBoxLayout(self.quality_widget)
        quality_layout.setContentsMargins(0, 0, 0, 0)
        quality_layout.addWidget(QLabel("Chất lượng:"))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(list(VIDEO_QUALITIES.values()))
        self.quality_combo.setMinimumWidth(180)
        self.quality_combo.setMaximumWidth(220)
        quality_layout.addWidget(self.quality_combo)
        quality_layout.addStretch()
        options_layout.addWidget(self.quality_widget)

        self.audio_options_widget = QWidget()
        audio_options_layout = QHBoxLayout(self.audio_options_widget)
        audio_options_layout.setContentsMargins(0, 0, 0, 0)
        audio_options_layout.addWidget(QLabel("Định dạng:"))
        self.audio_format_combo = QComboBox()
        self.audio_format_combo.addItems(list(AUDIO_FORMATS.values()))
        self.audio_format_combo.setMinimumWidth(110)
        self.audio_format_combo.setMaximumWidth(160)
        audio_options_layout.addWidget(self.audio_format_combo)
        audio_options_layout.addSpacing(16)
        audio_options_layout.addWidget(QLabel("Bitrate:"))
        self.audio_bitrate_combo = QComboBox()
        self.audio_bitrate_combo.addItems(list(AUDIO_BITRATES.values()))
        self.audio_bitrate_combo.setMinimumWidth(120)
        self.audio_bitrate_combo.setMaximumWidth(140)
        audio_options_layout.addWidget(self.audio_bitrate_combo)
        audio_options_layout.addStretch()
        self.audio_options_widget.hide()
        options_layout.addWidget(self.audio_options_widget)

        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Thư mục lưu:"))
        self.path_input = QLineEdit()
        self.path_input.setText(self.config.get("download_path", DEFAULT_DOWNLOAD_PATH))
        self.path_input.setReadOnly(True)
        self.path_input.setMinimumWidth(260)
        self.browse_btn = QPushButton("📁 Chọn")
        self.browse_btn.setObjectName("primaryButton")
        self.browse_btn.setMinimumWidth(100)
        self.browse_btn.setMaximumWidth(100)
        self.browse_btn.clicked.connect(self._on_browse_clicked)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_btn)
        options_layout.addLayout(path_layout)

        download_layout = QHBoxLayout()
        self.download_btn = QPushButton("⬇ Tải xuống")
        self.download_btn.setMinimumHeight(40)
        self.download_btn.setMinimumWidth(120)
        self.download_btn.setMaximumWidth(150)
        self.download_btn.setObjectName("successButton")
        self.download_btn.clicked.connect(self._on_download_clicked)
        self.download_btn.setEnabled(False)
        download_layout.addWidget(self.download_btn)

        self.open_folder_btn = QPushButton("📁 Mở thư mục")
        self.open_folder_btn.setObjectName("outlineButton")
        self.open_folder_btn.setMinimumWidth(140)
        self.open_folder_btn.setEnabled(False)
        self.open_folder_btn.clicked.connect(self._on_open_folder_clicked)
        download_layout.addWidget(self.open_folder_btn)

        self.open_file_btn = QPushButton("📄 Mở file")
        self.open_file_btn.setObjectName("outlineButton")
        self.open_file_btn.setMinimumWidth(110)
        self.open_file_btn.setEnabled(False)
        self.open_file_btn.clicked.connect(self._on_open_file_clicked)
        download_layout.addWidget(self.open_file_btn)

        download_layout.addStretch()
        options_layout.addLayout(download_layout)

        layout.addWidget(options_frame)

        progress_frame = QFrame()
        progress_frame.setObjectName("card")
        progress_layout = QVBoxLayout(progress_frame)
        progress_layout.setSpacing(8)

        progress_top_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMinimumHeight(18)
        progress_top_layout.addWidget(self.progress_bar)
        self.progress_percent_label = QLabel("0%")
        self.progress_percent_label.setProperty("type", "secondary")
        self.progress_percent_label.setMinimumWidth(50)
        self.progress_percent_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        progress_top_layout.addWidget(self.progress_percent_label)
        progress_layout.addLayout(progress_top_layout)

        progress_info_layout = QHBoxLayout()
        self.progress_speed_label = QLabel("Tốc độ: -")
        self.progress_speed_label.setProperty("type", "secondary")
        self.progress_eta_label = QLabel("Còn lại: -")
        self.progress_eta_label.setProperty("type", "secondary")
        self.progress_downloaded_label = QLabel("Đã tải: -")
        self.progress_downloaded_label.setProperty("type", "secondary")
        progress_info_layout.addWidget(self.progress_speed_label)
        progress_info_layout.addWidget(self.progress_eta_label)
        progress_info_layout.addWidget(self.progress_downloaded_label)
        progress_layout.addLayout(progress_info_layout)

        self.progress_info_label = QLabel("Sẵn sàng để tải")
        self.progress_info_label.setProperty("type", "secondary")
        progress_layout.addWidget(self.progress_info_label)

        layout.addWidget(progress_frame)

        self._on_type_changed()
        self._reset_progress()
        
        return scroll
    
    def _create_history_tab(self) -> QWidget:
        """Tạo tab lịch sử"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Lịch sử tải xuống")
        title.setProperty("type", "title")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # History table
        self.history_table = QTableWidget()
        self.history_table.setObjectName("historyTable")
        self.history_table.verticalHeader().setVisible(True)
        self.history_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Thời gian", "Tiêu đề", "Loại", "Chất lượng", "Kích thước"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.history_table)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Làm mới")
        refresh_btn.setObjectName("primaryButton")
        refresh_btn.clicked.connect(self._refresh_history)
        
        delete_btn = QPushButton("🗑️ Xóa mục")
        delete_btn.setObjectName("dangerButton")
        delete_btn.clicked.connect(self._on_delete_history_clicked)
        
        clear_btn = QPushButton("🗑️ Xóa toàn bộ")
        clear_btn.setObjectName("dangerButton")
        clear_btn.clicked.connect(self._on_clear_history_clicked)
        
        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(clear_btn)
        
        layout.addLayout(btn_layout)
        
        # Load history
        self._refresh_history()
        
        return tab
    
    def _create_settings_tab(self) -> QWidget:
        """Tạo tab cài đặt"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Cài đặt")
        title.setProperty("type", "title")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Theme selection
        theme_label = QLabel("Chế độ:")
        theme_label.setProperty("type", "title")
        layout.addWidget(theme_label)
        
        theme_layout = QHBoxLayout()
        
        self.theme_light_btn = QPushButton("☀️ Light")
        self.theme_light_btn.setCheckable(True)
        self.theme_light_btn.setChecked(self.theme == "light")
        self.theme_light_btn.setMaximumWidth(150)
        self.theme_light_btn.setObjectName("toggleButton")
        self.theme_light_btn.clicked.connect(lambda: self._on_theme_changed("light"))
        
        self.theme_dark_btn = QPushButton("🌙 Dark")
        self.theme_dark_btn.setCheckable(True)
        self.theme_dark_btn.setChecked(self.theme == "dark")
        self.theme_dark_btn.setMaximumWidth(150)
        self.theme_dark_btn.setObjectName("toggleButton")
        self.theme_dark_btn.clicked.connect(lambda: self._on_theme_changed("dark"))
        
        theme_layout.addWidget(self.theme_light_btn)
        theme_layout.addWidget(self.theme_dark_btn)
        theme_layout.addStretch()
        layout.addLayout(theme_layout)
        
        # FFmpeg info
        ffmpeg_label = QLabel("FFmpeg:")
        ffmpeg_label.setProperty("type", "title")
        layout.addWidget(ffmpeg_label)
        
        self.ffmpeg_info_label = QLabel()
        self.ffmpeg_info_label.setProperty("type", "secondary")
        layout.addWidget(self.ffmpeg_info_label)
        
        # About

        layout.addSpacing(30)
        
        about_label = QLabel("Về ứng dụng")
        about_label.setProperty("type", "title")
        layout.addWidget(about_label)
        
        about_text = QTextEdit()
        about_text.setObjectName("aboutText")
        about_text.setMarkdown("""
        YouTube Downloader

        Phiên bản: v1.0.0

        Tác giả 
        Developed by Panchi

        Giấy phép  
        MIT License
        """)
        about_text.setReadOnly(True)

        if self.theme == "light":
            about_text.setStyleSheet("""
                QTextEdit#aboutText {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #dddddd;
                    border-radius: 12px;
                    padding: 14px;
                    font-size: 14px;
                }
            """)

        layout.addWidget(about_text)
        
        layout.addStretch()
        
        return tab
    
    def _check_ffmpeg(self) -> None:
        """Kiểm tra FFmpeg"""
        ffmpeg_bin = get_ffmpeg_bin_path()

        if ffmpeg_bin:
            status = "✅ Đã tích hợp FFmpeg portable"
            color = self.colors['success']
        elif check_ffmpeg_installed():
            status = "✅ FFmpeg từ hệ thống"
            color = self.colors['success']
        else:
            status = "❌ Chưa tìm thấy FFmpeg"
            color = self.colors['error']
        
        self.ffmpeg_info_label.setText(status)
        self.ffmpeg_info_label.setStyleSheet(f"color: {color};")
        
    def _on_type_changed(self) -> None:
        """Xử lý khi thay đổi loại tải"""
        is_video = self.type_video_radio.isChecked()

        if not is_video and not self.type_audio_radio.isChecked():
            self.type_video_radio.setChecked(True)
            is_video = True
        
        self.quality_widget.setVisible(is_video)
        self.audio_options_widget.setVisible(not is_video)

    def _reset_progress(self) -> None:
        """Đặt lại trạng thái progress"""
        self.progress_bar.setValue(0)
        self.progress_percent_label.setText("0%")
        self.progress_speed_label.setText("Tốc độ: -")
        self.progress_eta_label.setText("Còn lại: -")
        self.progress_downloaded_label.setText("Đã tải: -")
        self.progress_info_label.setText("Sẵn sàng để tải")

    def _reset_video_info(self) -> None:
        """Đặt lại thông tin video"""
        self.title_label.setText("Chưa phân tích")
        self.channel_label.setText("")
        self.duration_label.setText("")
        self.max_quality_label.setText("Chất lượng tối đa: -")
        self.size_label.setText("Dung lượng ước tính: -")
        self.thumbnail_label.setPixmap(QPixmap())
        self.thumbnail_label.setText("Chưa có thumbnail")

    def _on_reset_clicked(self) -> None:
        """Xóa link và reset giao diện"""
        self.url_input.clear()
        self.current_video_info = None
        self.last_downloaded_file = ""
        self.download_btn.setEnabled(False)
        self.open_folder_btn.setEnabled(False)
        self.open_file_btn.setEnabled(False)
        self.url_input.setReadOnly(False)
        self.analyze_btn.setEnabled(True)
        self.analyze_btn.setText("🔍 Phân tích link")
        self.quality_combo.clear()
        self.quality_combo.addItems(list(VIDEO_QUALITIES.values()))
        self.audio_format_combo.setCurrentIndex(0)
        self.audio_bitrate_combo.clear()
        self.audio_bitrate_combo.addItems(list(AUDIO_BITRATES.values()))
        self._reset_video_info()
        self._reset_progress()

    def _on_open_file_clicked(self) -> None:
        """Mở file vừa tải"""
        if self.last_downloaded_file and os.path.exists(self.last_downloaded_file):
            os.startfile(self.last_downloaded_file)
        else:
            self.show_warning("Lỗi", "File không tồn tại")

    def _update_available_video_qualities(self, info: dict) -> None:
        """Cập nhật danh sách chất lượng video theo định dạng có sẵn"""
        formats = info.get("formats", [])
        heights = set()

        for fmt in formats:
            height = fmt.get("height")
            vcodec = fmt.get("vcodec")
            if height and vcodec and vcodec != "none":
                heights.add(height)

        max_height = max(heights) if heights else 0

        self.quality_combo.clear()
        self.quality_combo.addItem("Chất lượng tốt nhất")

        if max_height >= 2160:
            self.quality_combo.addItem("4K (2160p)")
        if max_height >= 1440:
            self.quality_combo.addItem("2K (1440p)")
        if max_height >= 1080:
            self.quality_combo.addItem("1080p")
        if max_height >= 720:
            self.quality_combo.addItem("720p")
        if max_height >= 480:
            self.quality_combo.addItem("480p")
        if max_height >= 360:
            self.quality_combo.addItem("360p")

    def _update_available_audio_bitrates(self, info: dict) -> None:
        """Cập nhật danh sách bitrate audio theo định dạng có sẵn"""
        formats = info.get("formats", [])
        max_abr = 0

        for fmt in formats:
            acodec = fmt.get("acodec")
            abr = fmt.get("abr")
            if acodec and acodec != "none" and abr:
                max_abr = max(max_abr, int(abr))

        self.audio_bitrate_combo.clear()

        if max_abr <= 0:
            self.audio_bitrate_combo.addItems(["128 kbps", "192 kbps", "320 kbps"])
        else:
            self.audio_bitrate_combo.addItem("128 kbps")
            if max_abr >= 128:
                self.audio_bitrate_combo.addItem("192 kbps")
            if max_abr >= 160:
                self.audio_bitrate_combo.addItem("320 kbps")

    def _get_max_quality_label(self, info: dict) -> str:
        """Lấy label chất lượng tối đa từ formats"""
        formats = info.get("formats", [])
        heights = [fmt.get("height") for fmt in formats if fmt.get("height")]
        max_height = max(heights) if heights else 0

        if max_height >= 2160:
            return "4K (2160p)"
        if max_height >= 1440:
            return "2K (1440p)"
        if max_height >= 1080:
            return "1080p"
        if max_height >= 720:
            return "720p"
        if max_height >= 480:
            return "480p"
        if max_height >= 360:
            return "360p"
        return "-"

    def _get_estimated_size_label(self, info: dict) -> str:
        """Lấy dung lượng ước tính nếu có"""
        size = info.get("filesize") or info.get("filesize_approx")
        if size:
            return format_bytes(size)
        return "-"
    
    def _on_analyze_clicked(self) -> None:
        """Xử lý khi nhấn nút phân tích"""
        url = self.url_input.text().strip()
        
        if not url:
            self.show_warning("Lỗi", "Vui lòng nhập link YouTube")
            return
        
        if not is_valid_youtube_url(url):
            self.show_warning("Lỗi", "URL không phải là link YouTube hợp lệ")
            return
        
        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setText("⏳ Đang phân tích...")
        
        # Tạo worker
        self.analyze_worker = AnalyzeWorker(url)
        self.analyze_worker.success.connect(self._on_analyze_success)
        self.analyze_worker.error.connect(self._on_analyze_error)
        self.analyze_worker.finished.connect(self._on_analyze_finished)
        self.analyze_worker.start()
    
    def _on_analyze_success(self, info: dict) -> None:
        """Xử lý khi phân tích thành công"""
        self.current_video_info = info
        
        # Cập nhật thông tin
        self.title_label.setText(info['title'])
        self.channel_label.setText(f"Kênh: {info['channel']}")
        self.duration_label.setText(f"Thời lượng: {format_seconds(info['duration'])}")
        self.max_quality_label.setText(f"Chất lượng tối đa: {self._get_max_quality_label(info)}")
        self.size_label.setText(f"Dung lượng ước tính: {self._get_estimated_size_label(info)}")
        
        # Tải và hiển thị thumbnail
        try:
            thumbnail_url = info['thumbnail']
            if thumbnail_url:
                response = requests.get(thumbnail_url, timeout=5)
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                scaled_pixmap = pixmap.scaledToWidth(220, Qt.TransformationMode.SmoothTransformation)
                self.thumbnail_label.setPixmap(scaled_pixmap)
        except Exception as e:
            print(f"Lỗi tải thumbnail: {e}")

        self._update_available_video_qualities(info)
        self._update_available_audio_bitrates(info)
        
        # Bật nút tải
        self.download_btn.setEnabled(True)
        self.open_folder_btn.setEnabled(False)
        self.open_file_btn.setEnabled(False)
        
        self.show_info("Thành công", "Phân tích link thành công!")
    
    def _on_analyze_error(self, error: str) -> None:
        """Xử lý lỗi khi phân tích"""
        self.show_error("Lỗi", error)
    
    def _on_analyze_finished(self) -> None:
        """Xử lý khi phân tích hoàn thành"""
        self.analyze_btn.setEnabled(True)
        self.analyze_btn.setText("🔍 Phân tích link")
    
    def _on_browse_clicked(self) -> None:
        """Xử lý khi nhấn nút chọn thư mục"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Chọn thư mục lưu",
            self.path_input.text()
        )
        
        if folder:
            self.path_input.setText(folder)
            self.config["download_path"] = folder
            save_config(self.config)
    
    def _on_download_clicked(self) -> None:
        """Xử lý khi nhấn nút tải"""
        if not self.current_video_info:
            self.show_warning("Lỗi", "Vui lòng phân tích link trước")
            return
        
        url = self.url_input.text().strip()
        output_path = self.path_input.text()
        
        if not ensure_dir_exists(output_path):
            self.show_error("Lỗi", "Không thể truy cập thư mục lưu")
            return
        
        # Lấy tùy chọn
        is_video = self.type_video_radio.isChecked()
        
        if is_video:
            quality_text = self.quality_combo.currentText()
            quality_key = [k for k, v in VIDEO_QUALITIES.items() if v == quality_text][0]
            download_type = "video"
            quality = quality_key
        else:
            format_text = self.audio_format_combo.currentText()
            format_key = [k for k, v in AUDIO_FORMATS.items() if v == format_text][0]
            bitrate_text = self.audio_bitrate_combo.currentText()
            bitrate_key = [k for k, v in AUDIO_BITRATES.items() if v == bitrate_text][0]
            download_type = "audio"
            quality = format_key
        
        # Cấu hình lưu
        self.config["video_quality"] = quality_key if is_video else ""
        self.config["audio_format"] = format_key if not is_video else ""
        self.config["audio_bitrate"] = bitrate_key if not is_video else ""
        save_config(self.config)
        
        # Disable các control
        self.download_btn.setEnabled(False)
        self.open_folder_btn.setEnabled(False)
        self.open_file_btn.setEnabled(False)
        self.analyze_btn.setEnabled(False)
        self.url_input.setReadOnly(True)
        
        # Tạo worker tải
        if is_video:
            self.download_worker = DownloadWorker(
                url, output_path, download_type, quality,
            )
        else:
            self.download_worker = DownloadWorker(
                url, output_path, download_type,
                audio_format=quality,
                audio_bitrate=bitrate_key,
            )
        
        self.download_worker.progress.connect(self._on_download_progress)
        self.download_worker.success.connect(self._on_download_success)
        self.download_worker.error.connect(self._on_download_error)
        self.download_worker.finished.connect(self._on_download_finished)
        self.download_worker.start()
    
    def _on_download_progress(self, data: dict) -> None:
        """Xử lý tiến độ tải"""
        status = data.get('status')
        
        if status == 'downloading':
            percent = data.get('percent', 0)
            downloaded = data.get('downloaded', '0 B')
            total = data.get('total', '0 B')
            speed = data.get('speed', '0 B')
            eta = data.get('eta') or 0
            
            self.progress_bar.setValue(percent)
            self.progress_percent_label.setText(f"{percent}%")
            
            eta_str = format_seconds(eta) if eta > 0 else "Tính toán..."
            info_text = f"{downloaded} / {total} - Tốc độ: {speed} - Còn: {eta_str}"
            self.progress_info_label.setText(info_text)
            self.progress_speed_label.setText(f"Tốc độ: {speed}")
            self.progress_eta_label.setText(f"Còn lại: {eta_str}")
            self.progress_downloaded_label.setText(f"Đã tải: {downloaded} / {total}")
        
        elif status == 'finished':
            self.progress_bar.setValue(100)
            self.progress_percent_label.setText("100%")
            self.progress_info_label.setText("Đang xử lý...")
        
        elif status == 'log':
            message = data.get('message', '')
            if message:
                self.progress_info_label.setText(message)
    
    def _on_download_success(self, file_path: str) -> None:
        """Xử lý khi tải thành công"""
        self.last_downloaded_file = file_path
        self.open_folder_btn.setEnabled(True)
        self.open_file_btn.setEnabled(True)
        # Cập nhật lịch sử
        info = self.current_video_info
        is_video = self.type_video_radio.isChecked()
        
        quality_text = self.quality_combo.currentText() if is_video else self.audio_format_combo.currentText()
        
        try:
            file_size = os.path.getsize(file_path)
        except:
            file_size = 0
        
        self.history.add(
            url=self.url_input.text(),
            title=info['title'],
            channel=info['channel'],
            duration=info['duration'],
            type_="video" if is_video else "audio",
            quality=self.quality_combo.currentText() if is_video else self.audio_bitrate_combo.currentText(),
            format_=quality_text,
            file_path=file_path,
            file_size=file_size
        )
        
        self.show_info("Thành công", f"Tải xong!\n{file_path}")
        
        self.progress_info_label.setText("Tải thành công!")
    
    def _on_download_error(self, error: str) -> None:
        """Xử lý lỗi tải"""
        self.show_error("Lỗi", error)
        self.progress_info_label.setText("Lỗi tải xuống")
        self.open_folder_btn.setEnabled(False)
        self.open_file_btn.setEnabled(False)
    
    def _on_download_finished(self) -> None:
        """Xử lý khi tải hoàn thành"""
        self.download_btn.setEnabled(True)
        self.analyze_btn.setEnabled(True)
        self.url_input.setReadOnly(False)
    
    def _on_open_folder_clicked(self) -> None:
        """Mở thư mục lưu"""
        output_path = self.path_input.text()
        if os.path.exists(output_path):
            os.startfile(output_path)
        else:
            self.show_warning("Lỗi", "Thư mục không tồn tại")
    
    def _refresh_history(self) -> None:
        """Làm mới lịch sử"""
        history_list = self.history.get_history()
        
        self.history_table.setRowCount(len(history_list))
        
        for row, entry in enumerate(history_list):
            try:
                from datetime import datetime
                timestamp = datetime.fromisoformat(entry['timestamp'])
                time_str = timestamp.strftime("%d/%m/%Y %H:%M:%S")
            except:
                time_str = "N/A"
            
            title = entry.get('title', 'N/A')[:50]
            type_str = "Video" if entry.get('type') == 'video' else "Âm thanh"
            quality = entry.get('quality', 'N/A')
            size_str = format_bytes(entry.get('file_size', 0))
            
            self.history_table.setItem(row, 0, QTableWidgetItem(time_str))
            self.history_table.setItem(row, 1, QTableWidgetItem(title))
            self.history_table.setItem(row, 2, QTableWidgetItem(type_str))
            self.history_table.setItem(row, 3, QTableWidgetItem(quality))
            self.history_table.setItem(row, 4, QTableWidgetItem(size_str))
    
    def _on_delete_history_clicked(self) -> None:
        """Xóa một mục lịch sử"""
        row = self.history_table.currentRow()
        if row < 0:
            self.show_warning("Lỗi", "Vui lòng chọn mục để xóa")
            return
        
        reply = QMessageBox.question(self, "Xác nhận", "Xóa mục lịch sử này?")
        if reply == QMessageBox.StandardButton.Yes:
            entry_id = row + 1
            self.history.remove_entry(entry_id)
            self._refresh_history()
    
    def _on_clear_history_clicked(self) -> None:
        """Xóa toàn bộ lịch sử"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Xác nhận")
        msg.setText("Xóa toàn bộ lịch sử?")

        yes_btn = msg.addButton("Yes", QMessageBox.ButtonRole.YesRole)
        no_btn = msg.addButton("No", QMessageBox.ButtonRole.NoRole)
        msg.setDefaultButton(no_btn)

        if self.theme == "light":
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #ffffff;
                    color: #000000;
                }

                QMessageBox QLabel {
                    color: #000000;
                    background-color: transparent;
                }

                QMessageBox QPushButton {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #000000;
                    border-radius: 5px;
                    padding: 4px 16px;
                    min-width: 70px;
                    min-height: 24px;
                }

                QMessageBox QPushButton:hover {
                    background-color: #f2f2f2;
                }
            """)

        msg.exec()

        if msg.clickedButton() == yes_btn:
            self.history.clear_history()
            self._refresh_history()
    
    def _on_theme_changed(self, theme: str) -> None:
        """Thay đổi theme"""
        self.theme = theme
        self.config["theme"] = theme
        save_config(self.config)
        
        # Cập nhật UI
        self.theme_light_btn.setChecked(theme == "light")
        self.theme_dark_btn.setChecked(theme == "dark")
        
        # Áp dụng stylesheet mới
        self.setStyleSheet(get_stylesheet(theme))
        
        self.show_info("Thành công", "Vui lòng khởi động lại ứng dụng để áp dụng theme")
    
    
