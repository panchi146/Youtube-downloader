# 🎵 YouTube Downloader Pro — Công cụ tải Video & MP3 chuyên nghiệp

Một ứng dụng desktop mạnh mẽ dành cho Windows, giúp tải video YouTube với chất lượng gốc, tải nhạc MP3 nhanh chóng, phân tích link thông minh và quản lý lịch sử tải xuống một cách chuyên nghiệp.

Ứng dụng được xây dựng bằng Python + PyQt5, kết hợp yt-dlp và FFmpeg để mang lại trải nghiệm tải xuống ổn định, nhanh và dễ sử dụng.
---

# 🚀 Hướng dẫn cài đặt

---

## Step 1: Clone Source Code

```bash
git clone https://github.com/panchi146/Youtube-downloader.git
cd youtube_downloader
```

---

## Step 2: Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

Nếu gặp lỗi:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Step 3: Cài đặt FFmpeg

Tải trực tiếp tại:

Giải nén vào:

```text
C:\ffmpeg
```

Thêm vào PATH của Windows:

* Nhấn Windows
* Tìm: `Environment Variables`
* Chọn: `Edit environment variables`
* Chọn: `Environment Variables`
* Chỉnh biến `PATH`
* Thêm:

```text
C:\ffmpeg\bin
```

Kiểm tra:

```bash
ffmpeg -version
```

Nếu hiển thị version → thành công.

---



---

# 🏗️ Cấu trúc dự án

```text
youtube_downloader/
├── main.py
├── requirements.txt
├── README.md
├── QUICKSTART.md
├── BUILD.md
│
├── app/
│   ├── ui/
│   │   ├── main_window.py
│   │   └── styles.py
│   │
│   ├── core/
│   │   ├── downloader.py
│   │   ├── analyzer.py
│   │   └── history.py
│   │
│   ├── workers/
│   │   ├── download_worker.py
│   │   └── analyze_worker.py
│   │
│   └── utils/
│       ├── helpers.py
│       └── config.py
│
├── assets/
│   ├── icon.png
│   └── icon.ico
│
├── data/
│   ├── download_history.json
│   └── config.json
│
└── ffmpeg/
```
---

# 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=panchi146/Youtube-downloader&type=Date)](https://star-history.com/#panchi146/Youtube-downloader&Date)

Nếu dự án hữu ích, hãy để lại một ⭐ trên GitHub.

Điều đó giúp dự án phát triển mạnh hơn và cải thiện nhiều tính năng trong tương lai.

---

