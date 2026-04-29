# 🏗️ Cấu Trúc Dự án

```
youtube_downloader_app/
├── main.py                         # Điểm chạy chính của ứng dụng
├── requirements.txt                # Danh sách thư viện Python cần cài
├── README.md                       # Hướng dẫn sử dụng đầy đủ
├── QUICKSTART.md                   # Hướng dẫn chạy nhanh
├── BUILD.md                        # Hướng dẫn build ra file .exe
├── DEVELOPMENT.md                  # Tài liệu cho developer
│
├── app/                            # Mã nguồn chính của ứng dụng
│   ├── __init__.py                 # Đánh dấu app là Python package
│   │
│   ├── ui/                         # Phần giao diện người dùng
│   │   ├── __init__.py
│   │   ├── main_window.py          # Cửa sổ chính, nút bấm, tab, xử lý UI
│   │   └── styles.py               # Giao diện màu sắc, dark/light mode, CSS Qt
│   │
│   ├── core/                       # Logic xử lý chính
│   │   ├── __init__.py
│   │   ├── downloader.py           # Tải video/audio bằng yt-dlp + FFmpeg
│   │   ├── analyzer.py             # Phân tích link YouTube, lấy title, thumbnail, format
│   │   └── history.py              # Quản lý lịch sử tải xuống
│   │
│   ├── workers/                    # Luồng xử lý nền để UI không bị đơ
│   │   ├── __init__.py
│   │   ├── download_worker.py      # Thread tải file, gửi progress về UI
│   │   └── analyze_worker.py       # Thread phân tích link YouTube
│   │
│   └── utils/                      # Hàm tiện ích và cấu hình
│       ├── __init__.py
│       ├── helpers.py              # Format dung lượng, thời gian, kiểm tra URL, tìm FFmpeg
│       └── config.py               # Cấu hình app, theme, đường dẫn lưu, data path
│
├── assets/                         # Tài nguyên giao diện
│   ├── icon.png                    # Icon dạng ảnh PNG
│   └── icon.ico                    # Icon dùng khi build file .exe
│
├── data/                           # Dữ liệu sinh ra khi chạy source
│   ├── download_history.json       # Lịch sử tải xuống
│   └── config.json                 # Cài đặt người dùng
│
└── ffmpeg/                         # FFmpeg portable đi kèm app
    └── bin/
        ├── ffmpeg.exe              # Công cụ ghép video/audio, convert MP3/MP4
        └── ffprobe.exe             # Công cụ đọc thông tin file media

```
# 🚀 Quick Start - YouTube Downloader

Hướng dẫn nhanh để bắt đầu sử dụng ứng dụng trong 5 phút!

## ⚡ Cài đặt Nhanh (5 phút)

### 1. Cài đặt Dependencies

```bash
# Mở Command Prompt tại thư mục youtube_downloader_app
pip install -r requirements.txt
```

**Nếu lỗi**, thử:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Cài FFmpeg (1 phút)

Tải trực tiếp:
1. Tải: https://ffmpeg.org/download.html
2. Giải nén vào: `C:\ffmpeg`
3. Thêm vào PATH (Windows):
   - Nhấn `Windows key` → Gõ "Environment" → "Edit environment variables"
   - "Environment Variables" → New
   - Variable name: `PATH`
   - Variable value: `C:\ffmpeg\bin`
   - OK

Kiểm tra:
```bash
ffmpeg -version
```

### 3. Chạy Ứng dụng

```bash
python main.py
```
Xong! Ứng dụng sẽ khởi động 🎉


# Hướng dẫn Build .exe - YouTube Downloader

Hướng dẫn chi tiết để tạo file .exe từ mã nguồn Python để phân phối trên Windows.

## 📋 Yêu cầu

- Python 3.8+ đã cài đặt
- Tất cả dependencies từ `requirements.txt` đã cài đặt
- PyInstaller (sẽ cài dưới đây)

## 🔧 Các bước Build

### Bước 1: Cài đặt PyInstaller

```bash
pip install pyinstaller
```

Kiểm tra cài đặt thành công:
```bash
pyinstaller --version
```

### Bước 2: Prepare File Icon (Tuỳ chọn)

Nếu muốn có icon custom:

1. Chuẩn bị file icon `.ico` (256x256 px hoặc lớn hơn)
2. Đặt vào thư mục `assets/` với tên `icon.ico`

Để chuyển đổi `.png` sang `.ico`:
```bash
pip install pillow
python -c "from PIL import Image; Image.open('assets/icon.png').save('assets/icon.ico')"
```

### Bước 3: Build File .exe

```bash
python -m PyInstaller --onedir --windowed --name "YouTube Downloader" --icon=assets/icon.ico --add-data "ffmpeg;ffmpeg" --add-data "assets;assets" main.py
```

### Bước 4: Tìm File .exe

File .exe được tạo tại:
```
dist/YouTube Downloader/
```

## 🎨 Tạo Installer

Để tạo installer chuyên nghiệp, sử dụng **Inno Setup**:

### Bước 1: Cài đặt Inno Setup

Tải từ: https://jrsoftware.org/isdl.php

### Bước 2: Tạo Script Installer

Tạo file `installer.iss` lưu tại thư mục chứ hàm main:

```ini
#define MyAppName "YouTube Downloader"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Panchi"
#define MyAppExeName "YouTube Downloader.exe"

[Setup]
AppId={{F4D8C5F6-9D9A-4A4B-8A12-YOUTUBE-DOWNLOADER}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=installer_output
OutputBaseFilename=YouTube_Downloader_Setup
SetupIconFile=assets\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Tạo biểu tượng ngoài Desktop"; GroupDescription: "Tùy chọn:"; Flags: unchecked

[Files]
Source: "dist\YouTube Downloader\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Mở {#MyAppName}"; Flags: nowait postinstall skipifsilent
```

### Bước 3: Build Installer

Vào inno -> build -> Combile

File installer sẽ tạo tại: `output/YouTube_Downloader_Setup_v1.0.0.exe`


## 🎯 Tham số PyInstaller Hữu ích

| Tham số | Ý nghĩa |
|--------|---------|
| `--onefile` | Tạo 1 file .exe duy nhất |
| `--windowed` | Không hiển thị console window |
| `--icon` | Thêm icon |
| `--name` | Tên file .exe |
| `--add-data` | Thêm file dữ liệu |
| `--hidden-import` | Import thêm module |
| `--collect-all` | Collect tất cả thư viện con |
---

**Ghi chú**: Build process có thể mất vài phút tùy vào cấu hình máy.
## 📚 Resources

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)