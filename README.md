# Business Procurement Agent - Prototype tối giản

Project này minh họa luồng cơ bản nhất của một ứng dụng Python gọi LLM:

1. Đọc API key từ file `.env`.
2. Gửi một prompt tới OpenAI.
3. Nhận nội dung phản hồi.
4. In phản hồi ra terminal.

Project chưa sử dụng FastAPI, database, frontend, tool calling hoặc agent framework.

## Cấu trúc project

```text
.
|-- .env              # Chứa API key trên máy cá nhân, không commit lên Git
|-- .env.example      # Mẫu cấu hình để chia sẻ với người khác
|-- .gitignore        # Loại bỏ file bí mật và file tạm khỏi Git
|-- llm_client.py     # Đọc cấu hình và gọi OpenAI API
|-- main.py           # Tạo prompt, gọi hàm LLM và in kết quả
|-- requirements.txt  # Các thư viện Python cần cài
`-- README.md         # Hướng dẫn project
```

## Cách chạy

Yêu cầu Python 3.10 trở lên.

### 1. Tạo môi trường ảo

Trên PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Cài thư viện

```powershell
python -m pip install -r requirements.txt
```

### 3. Thêm API key

Mở file `.env` và thay `your_api_key_here` bằng API key thật:

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-5-mini
```

`OPENAI_MODEL` cho phép đổi model mà không cần sửa code.

### 4. Chạy chương trình

```powershell
python main.py
```

Sau khi API trả kết quả, nội dung sẽ được in ngay trong terminal.

## Luồng hoạt động

`main.py` tạo một prompt mẫu về đánh giá nhà cung cấp rồi gọi
`get_llm_response()` trong `llm_client.py`. Hàm này nạp biến môi trường từ
`.env`, tạo OpenAI client, gọi Responses API và trả về `response.output_text`.

Để thử prompt khác, chỉ cần sửa biến `prompt` trong `main.py`.

