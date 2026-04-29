# 🎵 YouTube Downloader Pro — Công cụ tải Video & MP3 chuyên nghiệp

Một ứng dụng desktop mạnh mẽ dành cho Windows, giúp tải video YouTube với chất lượng gốc, tải nhạc MP3 nhanh chóng, phân tích link thông minh và quản lý lịch sử tải xuống một cách chuyên nghiệp.

Ứng dụng được xây dựng bằng Python + PyQt5, kết hợp yt-dlp và FFmpeg để mang lại trải nghiệm tải xuống ổn định, nhanh và dễ sử dụng.

---

# ✨ Tính năng nổi bật

## 🎬 Tải Video YouTube chất lượng gốc

* Tải video YouTube với chất lượng cao nhất
* Hỗ trợ nhiều định dạng video
* Tự động ghép video + audio bằng FFmpeg
* Giữ nguyên chất lượng gốc từ nguồn phát

---

## 🎵 Tải MP3 âm thanh chất lượng cao

* Trích xuất audio từ video YouTube
* Xuất file MP3 chất lượng cao
* Tối ưu tốc độ tải xuống
* Phù hợp nghe nhạc, podcast, bài giảng

---

## 🔍 Phân tích link thông minh

* Tự động lấy tiêu đề video
* Hiển thị thumbnail
* Phân tích định dạng tải xuống
* Kiểm tra chất lượng video/audio trước khi tải

---

## ⚡ Download đa luồng ổn định

* Luồng nền riêng biệt giúp UI không bị đơ
* Thanh tiến trình tải trực quan
* Theo dõi trạng thái tải xuống realtime
* Tăng độ ổn định khi tải file lớn

---

## 🕘 Lịch sử tải xuống

* Lưu toàn bộ lịch sử tải file
* Theo dõi các video đã tải
* Quản lý dữ liệu tiện lợi
* Không bị mất lịch sử sau khi đóng app

---

## 🎨 Giao diện hiện đại

* Giao diện trực quan, dễ sử dụng
* Dark mode / Light mode
* Thiết kế tối ưu cho Windows
* Trải nghiệm giống phần mềm thương mại

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

## Step 4: Chạy ứng dụng

```bash
python main.py
```

Xong. Ứng dụng sẽ khởi động.

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

Cấu trúc dự án được tổ chức rõ ràng giữa UI, xử lý logic, worker thread và tiện ích hỗ trợ giúp dễ bảo trì và mở rộng. 

---

# 🔨 Build file .exe

## Cài PyInstaller

```bash
pip install pyinstaller
```

---

## Build ứng dụng

```bash
pyinstaller --onedir --windowed --name "YouTube Downloader" --icon=assets/icon.ico --add-data "ffmpeg;ffmpeg" --add-data "assets;assets" main.py
```

---

## File output

```text
dist/YouTube Downloader/
```

---

# 📦 Tạo bộ cài Setup (.exe)

Để tạo installer chuyên nghiệp, sử dụng:

## Inno Setup

Tải tại:

Sau đó compile file:

```text
installer.iss
```

Kết quả:

```text
YouTube_Downloader_Setup.exe
```

Người dùng chỉ cần tải và cài như phần mềm thông thường.

---

# ☕ Tác giả 

Được phát triển bởi:

**Panchi**

Email: phamvanchinhlqd@gmail.com

Nếu dự án này hữu ích cho bạn, hãy ⭐ repository để hỗ trợ phát triển thêm nhiều tính năng mới.

---

# 📝 Tuyên bố miễn trừ trách nhiệm

## Bảo mật là ưu tiên hàng đầu

Ứng dụng hoạt động hoàn toàn trên thiết bị người dùng.

* Không thu thập dữ liệu cá nhân
* Không theo dõi lịch sử sử dụng
* Không chia sẻ dữ liệu cho bên thứ ba

---

## Lưu ý sử dụng

Công cụ này chỉ phục vụ cho mục đích học tập, lưu trữ cá nhân và nghiên cứu.

Người dùng chịu trách nhiệm tuân thủ chính sách bản quyền nội dung từ nền tảng YouTube.

---

# 📜 Giấy phép

Dự án được phát hành theo giấy phép MIT License.

* Sử dụng cá nhân: miễn phí
* Sử dụng thương mại: cần liên hệ tác giả

Xem thêm tại file:

Xem tệp [LICENSE](./LICENSE) để biết thêm thông tin.

---

# 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=panchi146/Youtube-downloader&type=Date)](https://star-history.com/#panchi146/Youtube-downloader&Date)

Nếu dự án hữu ích, hãy để lại một ⭐ trên GitHub.

Điều đó giúp dự án phát triển mạnh hơn và cải thiện nhiều tính năng trong tương lai.

---

