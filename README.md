
# Hello! 👋

# Demo FastAPI với Xử lý Bất đồng bộ (Async Task Processing)

## 👋 Giới thiệu

Dự án này trình bày một ứng dụng FastAPI demo minh họa cách xử lý các tác vụ nặng (lâu thời gian, > timeout) (long-running tasks) một cách bất đồng bộ (asynchronously) mà không làm chặn luồng chính của API. Đây là một giải pháp đơn giản, phù hợp cho môi trường phát triển và demo trên Windows, sử dụng BackgroundTasks để chạy tác vụ nền và SQLite để lưu trữ kết quả bền vững.

## ✨ Tính năng

* RESTful API bằng FastAPI.
* Xử lý bất đồng bộ bằng background task.
* Lưu trữ kết quả tác vụ với SQLite.
* Trả về kết quả dạng HTML dễ nhìn.
* Hỗ trợ 2 loại tác vụ: tính toán và crawl.

## 📐 Kiến trúc

1. FastAPI tiếp nhận và xử lý request gửi tác vụ.
2. Tác vụ thực thi ở background (Fargate/Celery có thể thay thế sau).
3. Kết quả được lưu trong SQLite.
4. Client truy vấn theo session ID để lấy kết quả.

## 📂 Project Structure

```
async_api_demo/
├── app/
│   ├── __init__.py
│   ├── main.py              # 🚀 FastAPI app entrypoint
│   ├── tasks.py             # 🧰 Business logic (calculation / crawling)
│   ├── models.py            # 📊 SQLite table schema & operations
│   ├── schemas.py           # ✏️ Pydantic models (input/output validation)
├── results.db               # 📁 SQLite database file (autocreated)
├── README.md                # ℹ️ Project introduction and usage guide
├── requirements.txt         # 📦 Python dependencies
```

## 🚀 Yêu cầu

- Python 3.8+
- pip
- Internet (nếu sử dụng crawl)

## ⚙️ Cài đặt và Chạy

```bash
# Tạo thư mục và môi trường ảo
python -m venv venv
source venv/bin/activate  # Hoặc venv\Scripts\activate nếu dùng Windows
pip install -r requirements.txt

# Chạy server
uvicorn app.main:app --reload
```

### 🌐 Cài đặt Playwright Browser Binaries (nếu cần crawl nâng cao)
```bash
playwright install
```

## 🧪 Sử dụng API

### 1. Gửi Yêu cầu Tác vụ
```bash
curl -X POST "http://localhost:8000/submit-task?option=cal"
curl -X POST "http://localhost:8000/submit-task?option=crawl"
```

### 2. Truy vấn Kết quả (trả JSON)
```bash
curl "http://localhost:8000/get-result/{session_id}"
```

### 3. Xem Kết quả Dưới Dạng HTML
```bash
http://localhost:8000/view-result/{session_id}
```

## 🧱 Cấu trúc Dự án
Như trong thư mục `async_api_demo/` phía trên.

## 🛡️ Cân nhắc cho Môi trường Production

- Dùng Redis + Celery để xử lý hàng đợi thật sự.
- Thay SQLite bằng PostgreSQL hoặc DB chuyên dụng.
- Bảo mật session_id và chống abuse endpoint crawl.

